import { ValidationError } from '../services/api'
import './ValidationResults.css'

interface ValidationResultsProps {
  errors: ValidationError[]
}

export default function ValidationResults({ errors }: ValidationResultsProps) {
  if (errors.length === 0) {
    return null
  }

  return (
    <div className="validation-results">
      <div className="results-header">
        <h3>Validation Errors</h3>
        <span className="error-count">{errors.length} error{errors.length !== 1 ? 's' : ''} found</span>
      </div>
      <div className="results-table-container">
        <table className="results-table">
          <thead>
            <tr>
              <th>Row</th>
              <th>ID</th>
              <th>Column</th>
              <th>Error Message</th>
            </tr>
          </thead>
          <tbody>
            {errors.map((error, index) => (
              <tr key={index}>
                <td>{error.row_index ?? '—'}</td>
                <td>{error.id ?? '—'}</td>
                <td>
                  <span className="column-badge">{error.column}</span>
                </td>
                <td className="error-message-cell">{error.error_message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
