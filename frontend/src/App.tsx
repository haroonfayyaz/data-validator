import { useState } from 'react'
import FileUpload from './components/FileUpload'
import LoadingIndicator from './components/LoadingIndicator'
import SuccessBanner from './components/SuccessBanner'
import ValidationResults from './components/ValidationResults'
import { validateCsvFile, ValidationResponse } from './services/api'
import { getErrorMessage } from './utils/errorHandler'
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
    } catch (err) {
      setError(getErrorMessage(err))
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
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            <p>{error}</p>
          </div>
        )}

        {validationResult && validationResult.status === 'pass' && <SuccessBanner />}

        {validationResult && validationResult.status === 'fail' && (
          <ValidationResults errors={validationResult.errors} />
        )}
      </main>
    </div>
  )
}

export default App

