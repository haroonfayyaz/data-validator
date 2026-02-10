import './SuccessBanner.css'

export default function SuccessBanner() {
  return (
    <div className="success-banner">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <polyline points="20 6 9 17 4 12" />
      </svg>
      <div className="success-content">
        <h3>Validation Successful: Data is clean.</h3>
      </div>
    </div>
  )
}
