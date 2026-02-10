import { AxiosError } from 'axios'

export function getErrorMessage(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
      return 'Request timed out. Please check your connection and try again.'
    }

    if (error.code === 'ERR_NETWORK' || !error.response) {
      return 'Unable to connect to the server. Please check your internet connection and ensure the backend server is running.'
    }

    const status = error.response.status

    if (status === 400) {
      return error.response.data?.detail || 'Invalid request. Please check your file and try again.'
    }

    if (status === 413) {
      return 'File is too large. Please upload a smaller file.'
    }

    if (status === 500) {
      return 'Server error occurred. Please try again later or contact support if the problem persists.'
    }

    if (status >= 500) {
      return 'Server error occurred. Please try again later.'
    }

    if (status >= 400) {
      return error.response.data?.detail || 'An error occurred while processing your request.'
    }
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'An unexpected error occurred. Please try again.'
}
