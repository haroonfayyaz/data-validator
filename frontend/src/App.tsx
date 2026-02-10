import { useState } from 'react'
import FileUpload from './components/FileUpload'
import LoadingIndicator from './components/LoadingIndicator'
import { validateCsvFile, ValidationResponse } from './services/api'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [validationResult, setValidationResult] = useState<ValidationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    if (!selectedFile) return

    setLoading(true)
    setError(null)
    setValidationResult(null)

    try {
      const result = await validateCsvFile(selectedFile)
      setValidationResult(result)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while validating the file')
    } finally {
      setLoading(false)
    }
  }

  const handleFileChange = (file: File | null) => {
    setSelectedFile(file)
    setValidationResult(null)
    setError(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Data Validator</h1>
        <p>Upload a CSV file to validate your data</p>
      </header>
      <main className="app-main">
        <FileUpload onFileSelect={handleFileChange} selectedFile={selectedFile} />

        {selectedFile && !loading && (
          <div className="submit-section">
            <button className="submit-button" onClick={handleSubmit} type="button">
              Validate File
            </button>
          </div>
        )}

        {loading && <LoadingIndicator />}

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
      </main>
    </div>
  )
}

export default App

