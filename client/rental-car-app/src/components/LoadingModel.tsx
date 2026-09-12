import ReactDOM from 'react-dom';
import '../App.css';

export default function LoadingModal({ isOpen = false, message = 'Loading, please wait...' }) {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="modal-overlay" role="dialog" aria-modal="true">
      <div className="modal-card">
        <div className="spinner"></div>
        <div className="modal-text">{message}</div>
      </div>
    </div>,
    document.body
  );
}