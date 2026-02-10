import './LoadingIndicator.css'

export default function LoadingIndicator() {
  return (
    <div className="loading-indicator">
      <div className="spinner"></div>
      <p>Validating CSV file...</p>
    </div>
  )
}
