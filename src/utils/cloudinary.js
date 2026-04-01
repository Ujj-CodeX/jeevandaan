import axios from 'axios'

const CLOUD_NAME = 'djkpvzecv'        // ← from your .env
const UPLOAD_PRESET = 'jeevandaan_unsigned'  // ← create this in Cloudinary dashboard

export async function uploadToCloudinary(file, folder = 'jeevandaan') {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('upload_preset', UPLOAD_PRESET)
    formData.append('folder', folder)

    const response = await axios.post(
        `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/auto/upload`,
        formData
    )
    return response.data.secure_url  // ← returns URL
}
