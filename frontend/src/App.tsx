import { useState } from 'react'
import FileUpload from './components/FileUpload'

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  return (
    <div className="app">
      <header className="app-header">
        <h1>Data Validator</h1>
        <p>Upload a CSV file to validate your data</p>
      </header>
      <main className="app-main">
        <FileUpload onFileSelect={setSelectedFile} selectedFile={selectedFile} />
      </main>
    </div>
  )
}

export default App
