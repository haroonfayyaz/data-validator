import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface ValidationError {
  row_index: number | null
  id: number | null
  column: string
  error_message: string
}

export interface ValidationResponse {
  status: 'pass' | 'fail'
  errors: ValidationError[]
}

export async function validateCsvFile(file: File): Promise<ValidationResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post<ValidationResponse>('/validate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export default apiClient
