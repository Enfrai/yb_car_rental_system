import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import "../App.css";

/**
 * Single Toast Item Component
 * @param {string} message - Text message to display
 * @param {'info' | 'success' | 'error'} type - Style variant
 * @param {function} onClose - Callback invoked when the toast is dismissed
 * @param {number} duration - Auto-dismiss timeout in milliseconds (default: 3000ms)
 */

export default function Toast({ message = '', type = 'info', onClose = () => {}, duration = 3000 }) {
  if (!message) return null;

  useEffect(() => {
    const timer = setInterval(() => {
        if (onClose) onClose();
    }, duration);

    return () => { clearInterval(timer); }
  }, [onClose, duration]);

  return ReactDOM.createPortal(
    <div className="toast-container">
      <div className={`toast-item toast-${type}`} role="alert">
        <span>{message}</span>
        <button
          className="toast-close-btn"
          onClick={onClose}
          aria-label="Close"
        >
          ✕
        </button>
      </div>
    </div>,
    document.body,
  );
}
// ({
//   message = "",
//   type = "info",
//   onClose = () => {},
//   duration = 3000,
// }) {
//     const [toast, setToast] = userState<number>()
//   useEffect(() => {
//     // Automatically trigger the onClose callback after 3 seconds
//     const timer = setInterval(() => {
//       if (onClose) onClose();
//     }, duration);

//     // Clean up timer if component unmounts early
//     return () => clearTimeout(timer);
//   }, [onClose, duration]);

//   if (!message) return null;

//   // Render via Portal to ensure top-level z-index placement

// }
