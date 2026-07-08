#threads alternative due to production Glitch

from notifications.tasks import send_donor_notifications_task, create_notification_task


#

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
import threading  # ← KEY FIX: async notifications

from config.authentication import DonorJWTAuthentication
from config.permissions import IsDonor
from .models import AttenderRequest, PartnerDonorRequest,InterPartnerRequest
from .serializers import (
    AttenderRequestSerializer,
    AttenderRequestPublicSerializer,
    PartnerDonorRequestSerializer,
    PartnerDonorRequestPublicSerializer
)
from users.models import Donor
from partners.models import Partners
import jwt
import os
from notifications.helpers import notify_nearby_donors
from users.location import get_nearby_partners, get_nearby_donors
from .models import AttenderRating, DonorRating

from config.authentication import PartnerJWTAuthentication
from config.permissions import IsPartner
from config.authentication import AnyJWTAuthentication
from config.permissions import IsAuthenticated

from config.logger import get_logger

logger = get_logger(__name__)
# ─────────────────────────────────────────────────────────
#  HELPER: run any callable in a daemon thread so it never
#  blocks the HTTP response cycle.
# ─────────────────────────────────────────────────────────
def run_in_background(fn, *args, **kwargs):
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start()


# ════════════════════════════════════════════════════
#  ATTENDER REQUESTS
# ════════════════════════════════════════════════════

class AttenderRequestCreateView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request):
        donor = request.user

        if not donor.is_aadhaar_verified:
            if donor.total_requests_raised >= 1:

                logger.warning("attender_request_blocked_aadhaar_unverified", extra={
                    "donor_id": donor.id
                })
                return Response(
                    {'error': 'Verify Aadhaar to raise more requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = AttenderRequestSerializer(data=request.data)
        if serializer.is_valid():
            expires_at = timezone.now() + timedelta(hours=20)
            req = serializer.save(attender=donor, expires_at=expires_at)

            donor.total_requests_raised += 1
            donor.save()

            logger.info("attender_request_created", extra={
                "donor_id":     donor.id,
                "request_id":   str(req.reference_id),
                "blood_group":  req.blood_group,
                "urgency":      req.urgency,
                "hospital_name": req.hospital_name,
            })
 

            return Response({
                'message': 'Request raised successfully.',
                'reference_id': str(req.reference_id),
                'request': AttenderRequestSerializer(req).data
            }, status=status.HTTP_201_CREATED)

        logger.warning("attender_request_creation_invalid", extra={
            "donor_id": donor.id,  
              "errors" : serializer.errors
        })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttenderRequestListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        requests = AttenderRequest.objects.filter(
            status='pending'
        ).order_by('-created_at')

        urgency = request.query_params.get('urgency')
        blood_group = request.query_params.get('blood_group')

        if urgency:
            requests = requests.filter(urgency=urgency)
        if blood_group:
            requests = requests.filter(blood_group=blood_group)
        

        # No logger to reduce noise on cloud watcher

        return Response(
            AttenderRequestPublicSerializer(requests, many=True).data
        )


class AttenderRequestDetailView(APIView):

    def get(self, request, reference_id):
        try:
            req = AttenderRequest.objects.get(reference_id=reference_id)
            return Response(AttenderRequestSerializer(req).data)
        except AttenderRequest.DoesNotExist:
            logger.warning("attender_request_not_found", extra={
                "reference_id": reference_id        })
            return Response(
                {'error': 'Request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


# ════════════════════════════════════════════════════
#  PARTNER DONOR REQUESTS
# ════════════════════════════════════════════════════

class PartnerDonorRequestCreateView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        partner = request.user
        serializer = PartnerDonorRequestSerializer(data=request.data)

        if serializer.is_valid():
            expires_at = timezone.now() + timedelta(hours=12)
            req = serializer.save(partner=partner, expires_at=expires_at)

            # ── FIX: Replaced Background thread with Celery task for async notifications
            send_donor_notifications_task.delay(
              req.blood_group,
              str(partner.latitude),
              str(partner.longitude),
              f'Urgent! {req.blood_group} blood needed at {partner.hospital_name}. Please donate!',
              10,
            )

            logger.info("partner_donor_request_created", extra={
                "partner_id":   partner.id,
                "request_id":   req.id,
                "blood_group":  req.blood_group,
                "quantity":     req.quantity,
            })


            return Response({
                'message': 'Donor request raised successfully.',
                'request': PartnerDonorRequestSerializer(req).data
            }, status=status.HTTP_201_CREATED)

        logger.warning("partner_donor_request_creation_invalid", extra={
            "partner_id": partner.id,
            "errors": serializer.errors
        })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerDonorRequestListView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    DEFAULT_RADIUS_KM = 10
    FALLBACK_RADIUS_KM = 50

    def get(self, request):
        donor_lat   = request.query_params.get('lat')
        donor_lon   = request.query_params.get('lon')
        blood_group = request.query_params.get('blood_group')

        # ── FIX: select_related avoids N+1 on partner; only fetch open
        open_requests = PartnerDonorRequest.objects.filter(
            status='open'
        ).select_related('partner').order_by('-created_at')

        if blood_group:
            open_requests = open_requests.filter(blood_group=blood_group)

        if donor_lat and donor_lon:
            # ── FIX: get distinct partner ids from the queryset directly
            #    instead of loading all request objects into memory first.
            partner_ids = open_requests.values_list(
                'partner_id', flat=True
            ).distinct()

            partners_qs = Partners.objects.filter(
                id__in=partner_ids,
                latitude__isnull=False,
                longitude__isnull=False,
            )

            nearby_partners = get_nearby_partners(
                donor_lat, donor_lon,
                list(partners_qs),
                radius_km=self.DEFAULT_RADIUS_KM,
            )

            distance_map = {
                item['partner'].id: item['distance_km']
                for item in nearby_partners
            }
            nearby_partner_ids = list(distance_map.keys())

            open_requests = open_requests.filter(
                partner_id__in=nearby_partner_ids
            )

            data = PartnerDonorRequestPublicSerializer(
                open_requests, many=True
            ).data

            for item in data:
                item['distance_km'] = distance_map.get(
                    item.get('partner_id') or item.get('partner'), None
                )

            data = sorted(data, key=lambda x: x.get('distance_km') or 999)
            return Response(data)

        return Response(
            PartnerDonorRequestPublicSerializer(open_requests, many=True).data
        )


class PartnerDonorRequestListDetailView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    DEFAULT_RADIUS_KM = 10
    FALLBACK_RADIUS_KM = 50

    def get(self, request):
        donor_lat   = request.query_params.get('lat')
        donor_lon   = request.query_params.get('lon')
        blood_group = request.query_params.get('blood_group')

        open_requests = PartnerDonorRequest.objects.filter(
            status__in=['open', 'assigned']
        ).select_related('partner').order_by('-created_at')

        if blood_group:
            open_requests = open_requests.filter(blood_group=blood_group)

        if donor_lat and donor_lon:
            partner_ids = open_requests.values_list(
                'partner_id', flat=True
            ).distinct()

            partners_qs = Partners.objects.filter(
                id__in=partner_ids,
                latitude__isnull=False,
                longitude__isnull=False,
            )

            nearby_partners = get_nearby_partners(
                donor_lat, donor_lon,
                list(partners_qs),
                radius_km=self.DEFAULT_RADIUS_KM,
            )

            distance_map = {
                item['partner'].id: item['distance_km']
                for item in nearby_partners
            }
            nearby_partner_ids = list(distance_map.keys())

            open_requests = open_requests.filter(
                partner_id__in=nearby_partner_ids
            )

            data = PartnerDonorRequestPublicSerializer(
                open_requests, many=True
            ).data

            for item in data:
                item['distance_km'] = distance_map.get(
                    item.get('partner_id') or item.get('partner'), None
                )

            data = sorted(data, key=lambda x: x.get('distance_km') or 999)
            return Response(data)

        return Response(
            PartnerDonorRequestPublicSerializer(open_requests, many=True).data
        )


class DonorRequestDetailView(APIView):
    authentication_classes = [AnyJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        try:
            req = PartnerDonorRequest.objects.select_related(
                'partner', 'assigned_donor'
            ).get(id=request_id)

            return Response({
                'id': req.id,
                'hospital_name': req.partner.hospital_name,
                'city': req.partner.city,
                'blood_group': req.blood_group,
                'quantity': req.quantity,
                'status': req.status,
                'expires_at': req.expires_at,
                'created_at': req.created_at,
            })

        except PartnerDonorRequest.DoesNotExist:
            logger.warning("donor_request_not_found", extra={
                "request_id": request_id
            })
            return Response({'error': 'Request not found.'}, status=404)
        except Exception as e:
            logger.exception("donor_request_detail_error", extra={ "request_id": request_id })
            return Response({'error': str(e)}, status=500)


from .models import OTPCode

class DonorAcceptRequestView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request, request_id):
        try:
            donor = request.user

            if donor.is_locked:

                logger.warning("donor_request_accept_blocked_locked", extra={
                    "donor_id": donor.id ,
                    "request_id": request_id
                })
                return Response(
                    {'error': 'Your account is locked.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if not donor.is_aadhaar_verified:
                logger.warning("donor_request_accept_blocked_aadhaar_unverified", extra={
                    "donor_id": donor.id ,
                    "request_id": request_id
                })
                return Response(
                    {'error': 'Aadhaar verification required to accept donation requests.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        

            req = PartnerDonorRequest.objects.select_related('partner').get(
                id=request_id,
                status='open'
            )

            req.assigned_donor = donor
            req.status = 'assigned'
            req.save()

            OTPCode.objects.filter(request=req).delete()
            otp = OTPCode.objects.create(
                request=req,
                code=OTPCode.generate_code()
            )

            # ── FIX: notification in background
            create_notification_task.delay(
              partner_id=req.partner_id,
              notification_type='sms',
              trigger='donor_accepted',
               message=(
               f'Donor #{donor.id} has accepted your blood request '
                f'for {req.blood_group} ({req.quantity} units). '
               f'OTP: {otp.code}'
              ),
              status='pending',
            )

            logger.info("donor_accepted_request", extra={
                "donor_id":    donor.id,
                "request_id":  req.id,
                "partner_id":  req.partner.id,
                "blood_group": req.blood_group,
                "quantity":    req.quantity,
            })

            return Response({
                'message': 'Request accepted!',
                'otp_code': otp.code,
                'request': PartnerDonorRequestSerializer(req).data
            })

        except PartnerDonorRequest.DoesNotExist:
            logger.warning("donor_request_not_found", extra={
                "donor_id":   getattr(request.user, 'id', None),
                "request_id": request_id,
            })
            return Response(
                {'error': 'Request not found or already assigned.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception :
            logger.exception("donor_accept_request_error", extra={
                "donor_id":   getattr(request.user, 'id', None),
                "request_id": request_id,
            })
            return Response({'error': 'Something went wrong.'}, status=500)


class DonorCancelRequestView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request, request_id):
        try:
            donor = request.user

            req = PartnerDonorRequest.objects.get(
                id=request_id,
                assigned_donor=donor,
                status='assigned'
            )

            reason = request.data.get('reason')
            if not reason:
                logger.warning("donor_request_cancel_blocked_no_reason", extra={
                    "donor_id": donor.id,
                    "request_id": request_id})
                return Response(
                    {'error': 'Cancellation reason is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            req.status = 'open'
            req.assigned_donor = None   
            req.cancellation_reason = reason
            req.save()

            donor.reliability_score = max(0, donor.reliability_score - 10)
            donor.cancellation_count += 1

            if donor.cancellation_count >= 3:
                donor.is_locked = True
                donor.locked_until = timezone.now() + timedelta(days=30)
            
            logger.warning("donor_locked_after_cancellations", extra={
                    "donor_id":          donor.id,
                    "cancellation_count": donor.cancellation_count,
                    "locked_until":       str(donor.locked_until),
                })
            
            donor.save()

            logger.info("donor_cancelled_request", extra={
                "donor_id":          donor.id,
                "request_id":        req.id,
                "reason":            reason,
                "new_score":         donor.reliability_score,
                "cancellation_count": donor.cancellation_count,
            })

            return Response({
                'message': 'Request cancelled.',
                'reliability_score': donor.reliability_score
            })

        except PartnerDonorRequest.DoesNotExist:
            logger.warning("donor_request_not_found", extra={
                "donor_id":   getattr(request.user, 'id', None),
                "request_id": request_id,
            })
            return Response(
                {'error': 'Request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class FulfillAttenderRequestView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request, reference_id):
        try:
            partner = request.user

            req = AttenderRequest.objects.get(
                reference_id=reference_id,
                status='pending'
            )

            req.status = 'fulfilled'
            req.fulfilled_by = partner
            req.save()

            logger.info("attender_request_fulfilled", extra={
                "partner_id":   partner.id,
                "reference_id": str(reference_id),
                "blood_group":  req.blood_group,
                "quantity":     req.quantity,
            })

            return Response({
                'message': 'Request fulfilled successfully!',
                'reference_id': str(req.reference_id)
            })

        except AttenderRequest.DoesNotExist:

            logger.warning("attender_fulfill_not_found", extra={
                "partner_id":   getattr(request.user, 'id', None),
                "reference_id": str(reference_id),
            })

            return Response(
                {'error': 'Request not found or already fulfilled.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            logger.exception("attender_fulfill_error", extra={
                "partner_id":   getattr(request.user, 'id', None),
                "reference_id": str(reference_id),
            })
            return Response({'error': 'Something went wrong.'}, status=500)

class GetRequestOTPView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request, request_id):
        try:
            partner = request.user
            otp = OTPCode.objects.get(
                request_id=request_id,
                is_used=False,
                request__partner=partner
            )

            # WHY debug? → OTP fetch is read-only, high frequency during
            # donation session. Info level pe bahut noise hoga.
            logger.debug("otp_fetched", extra={
                "partner_id": partner.id,
                "request_id": request_id,
            })

            return Response({'otp_code': otp.code})

        except OTPCode.DoesNotExist:
            return Response({'otp_code': None}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def post(self, request):
        try:
            partner = request.user
            otp_code = request.data.get('otp_code')
            if not otp_code:
                logger.warning("otp_verify_missing_code", extra={
                    "partner_id": partner.id,
                })
                return Response(
                    {'error': 'OTP code is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                otp = OTPCode.objects.select_related('request').get(
                    code=otp_code, is_used=False, request__partner=partner
                )
            except OTPCode.DoesNotExist:
                
                logger.warning("otp_verify_invalid", extra={
                    "partner_id": partner.id,
                })
                return Response(
                    {'error': 'Invalid or already used OTP.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            otp.is_used = True
            otp.used_at = timezone.now()
            otp.save()

             # Timeline: donor_accepted → otp_verified → donation_verified
            logger.info("otp_verified_successfully", extra={
                "partner_id":  partner.id,
                "request_id":  otp.request.id,
                "blood_group": otp.request.blood_group,
                "quantity":    otp.request.quantity,
            })

            return Response({
                'message': 'OTP verified successfully!',
                'request_id': otp.request.id,
                'blood_group': otp.request.blood_group,
                'quantity': otp.request.quantity,
            })

        except Exception:
            logger.exception("otp_verify_error", extra={
                "partner_id": getattr(request.user, 'id', None),
            })
            return Response({'error': 'Something went wrong.'}, status=500)

class DonorPartnerRequestListView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        try:
            partner = request.user

            requests = PartnerDonorRequest.objects.filter(
                partner=partner,
                status__in=['open', 'assigned']
            ).select_related('partner', 'assigned_donor').order_by('-created_at')

            data = PartnerDonorRequestPublicSerializer(requests, many=True).data
            return Response(data)

        except Exception:
            logger.exception("partner_donor_request_list_error", extra={
                "partner_id": getattr(request.user, 'id', None),
            })
            return Response({"error": "Something went wrong."}, status=500)


# ════════════════════════════════════════════════════
#  RATINGS
# ════════════════════════════════════════════════════

class SubmitAttenderRatingView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request, reference_id):
        try:
            donor = request.user
            req = AttenderRequest.objects.select_related(
                'fulfilled_by'                 
            ).get(
                reference_id=reference_id,
                attender=donor,
                status='fulfilled'
            )

            if not req.fulfilled_by:
                logger.warning("attender_rating_no_partner", extra={
                    "donor_id":     donor.id,
                    "reference_id": str(reference_id),
                })
                return Response(
                    {'error': 'Request has no partner assigned. Cannot rate.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if AttenderRating.objects.filter(request=req).exists():

                logger.warning("attender_rating_already_submitted", extra={
                    "donor_id":     donor.id,
                    "reference_id": str(reference_id),
                })
                return Response(
                    {'error': 'Already rated this request.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stars = request.data.get('stars')
            review = request.data.get('review', '')
            has_complaint = request.data.get('has_complaint', False)
            complaint_type = request.data.get('complaint_type', None)
            complaint_detail = request.data.get('complaint_detail', '')

            if not stars or int(stars) not in range(1, 6):

                logger.warning("attender_rating_invalid_stars", extra={
                    "donor_id":     donor.id,
                    "stars_received": stars,
                })
                return Response(
                    {'error': 'Stars must be between 1 and 5.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            rating = AttenderRating.objects.create(
                attender=donor,
                partner=req.fulfilled_by,
                request=req,
                stars=int(stars),
                review=review,
                has_complaint=has_complaint,
                complaint_type=complaint_type if has_complaint else None,
                complaint_detail=complaint_detail if has_complaint else ''
            )

            if has_complaint:
                bad_count = AttenderRating.objects.filter(
                    partner=rating.partner,
                    has_complaint=True
                ).count()

                if bad_count >= 5:
                    rating.partner.is_live = False
                    rating.partner.save()

                    logger.warning("partner_suspended_complaints", extra={
                        "partner_id":  rating.partner.id,
                        "bad_count":   bad_count,
                        "trigger_donor": donor.id,
                    })
            
            logger.info("attender_rating_submitted", extra={
                "donor_id":       donor.id,
                "partner_id":     req.fulfilled_by.id,
                "reference_id":   str(reference_id),
                "stars":          int(stars),
                "has_complaint":  has_complaint,
                "complaint_type": complaint_type if has_complaint else None,
            })

            return Response({
                'message': 'Rating submitted successfully!',
                'stars': stars
            }, status=status.HTTP_201_CREATED)

        except AttenderRequest.DoesNotExist:
            logger.warning("attender_rating_request_not_found", extra={
                "donor_id":     getattr(request.user, 'id', None),
                "reference_id": str(reference_id),
            })
            return Response(
                {'error': 'Fulfilled request not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            logger.exception("attender_rating_error", extra={
                "donor_id":     getattr(request.user, 'id', None),
                "reference_id": str(reference_id),
            })
            return Response({'error': 'Something went wrong.'}, status=500)


class SubmitDonorRatingView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def post(self, request, request_id):
        try:
            donor = request.user

            req = PartnerDonorRequest.objects.select_related('partner').get(
                id=request_id,
                assigned_donor=donor,
                status='fulfilled'
            )

            if DonorRating.objects.filter(request=req).exists():
                logger.warning("donor_rating_already_submitted", extra={
                    "donor_id": donor.id,
                    "request_id": req.id
                })
                return Response(
                    {'error': 'You have already rated this request.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stars = int(request.data.get('stars', 5))
            review = request.data.get('review', '')

            if stars not in range(1, 6):
                logger.warning("donor_rating_invalid_stars", extra={
                    "donor_id": donor.id,
                    "stars_received": stars
                })
                return Response(
                    {'error': 'Stars must be between 1 and 5.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            DonorRating.objects.create(
                partner=req.partner,
                donor=donor,
                request=req,
                stars=stars,
                review=review
            )

            if stars <= 2:
                partner = req.partner
                bad_ratings = DonorRating.objects.filter(
                    partner=partner, stars__lte=2
                ).count()

                if bad_ratings >= 5:
                    partner.is_live = False
                    partner.save()

                logger.warning("partner_suspended_low_donor_rating", extra={
                    "partner_id": partner.id,               
                    "bad_ratings": bad_ratings,
                    "trigger_donor": donor.id,
                })
            

            logger.info("donor_rating_submitted", extra={
                "donor_id":   donor.id,
                "partner_id": req.partner.id,
                "request_id": request_id,
                "stars":      stars,
            })
            return Response({
                'message': 'Rating submitted successfully! Thank you'
            }, status=status.HTTP_201_CREATED)

        except PartnerDonorRequest.DoesNotExist:
            logger.warning("donor_rating_request_not_found", extra={
                "donor_id":   getattr(request.user, 'id', None),
                "request_id": request_id,
            })
            return Response(
                {'error': 'Fulfilled request not found or not assigned to you.'},
                status=status.HTTP_404_NOT_FOUND
            )
 
        except Exception:
            logger.exception("donor_rating_error", extra={
                "donor_id":   getattr(request.user, 'id', None),
                "request_id": request_id,
            })
            return Response({'error': 'Something went wrong.'}, status=500)


class MyAttenderRequestsView(APIView):
    authentication_classes = [DonorJWTAuthentication]
    permission_classes = [IsDonor]

    def get(self, request):
        try:
            donor = request.user

            requests = AttenderRequest.objects.filter(
                attender=donor
            ).order_by('-created_at')

            # ── FIX: batch fetch rated request ids — avoids N+1 per-request query
            rated_ids = set(
                AttenderRating.objects.filter(
                    request__attender=donor
                ).values_list('request_id', flat=True)
            )

            data = []
            for req in requests:
                data.append({
                    'reference_id': str(req.reference_id),
                    'patient_name': req.patient_name,
                    'blood_group': req.blood_group,
                    'quantity': req.quantity,
                    'urgency': req.urgency,
                    'hospital_name': req.hospital_name,
                    'city': req.city,
                    'status': req.status,
                    'is_rated': req.id in rated_ids,
                    'expires_at': req.expires_at,
                    'created_at': req.created_at,
                    'updated_at': req.updated_at,
                })

            return Response(data)

        except Exception:
            logger.exception("my_attender_requests_error", extra={
                "donor_id": getattr(request.user, 'id', None),
            })
            return Response(
                {'error': 'Something went wrong.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class PartnerHistoryView(APIView):
    authentication_classes = [PartnerJWTAuthentication]
    permission_classes = [IsPartner]

    def get(self, request):
        partner = request.user

        # 1. Donor requests jo partner ne raise ki (sab statuses — open/assigned/fulfilled/expired/cancelled)
        donor_requests = PartnerDonorRequest.objects.filter(
            partner=partner
        ).select_related('assigned_donor').order_by('-created_at')

        donor_data = [
            {
                'id': r.id,
                'blood_group': r.blood_group,
                'quantity': r.quantity,
                'status': r.status,
                'assigned_donor': r.assigned_donor.name if r.assigned_donor else None,
                'cancellation_reason': r.cancellation_reason,
                'created_at': r.created_at,
                'updated_at': r.updated_at,
            }
            for r in donor_requests
        ]

        # 2. Attender requests jo partner ne fulfill ki
        attender_fulfilled = AttenderRequest.objects.filter(
            fulfilled_by=partner
        ).order_by('-updated_at')

        attender_data = [
            {
                'reference_id': str(a.reference_id),
                'patient_name': a.patient_name,
                'blood_group': a.blood_group,
                'quantity': a.quantity,
                'urgency': a.urgency,
                'status': a.status,
                'created_at': a.created_at,
                'updated_at': a.updated_at,
            }
            for a in attender_fulfilled
        ]

        # 3. Inter-partner requests — sent bhi, received bhi
        from django.db.models import Q
        inter_requests = InterPartnerRequest.objects.filter(
            Q(requesting_partner=partner) | Q(fulfilling_partner=partner)
        ).select_related(
            'requesting_partner', 'fulfilling_partner', 'attender_request'
        ).order_by('-updated_at')

        inter_data = [
            {
                'id': i.id,
                'direction': 'sent' if i.requesting_partner_id == partner.id else 'received',
                'requesting_partner': i.requesting_partner.hospital_name,
                'fulfilling_partner': i.fulfilling_partner.hospital_name,
                'blood_group': i.blood_group,
                'quantity': i.quantity,
                'convenience_fee': str(i.convenience_fee),
                'status': i.status,
                'reference_id': str(i.attender_request.reference_id),
                'created_at': i.created_at,
                'updated_at': i.updated_at,
            }
            for i in inter_requests
        ]

        return Response({
            'donor_requests': donor_data,
            'attender_fulfilled': attender_data,
            'inter_partner_requests': inter_data,
        })