import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../App.css";

export default function View() {
  const navigate = useNavigate();

  const [fromDate, setFromDate] = useState(null);
  const [toDate, setToDate] = useState(null);

  const handleView = () => {
    if (!fromDate || !toDate) {
      alert("Please select both From and To dates");
      return;
    }

    // Navigate to result page with selected dates
    navigate("/view-result", {
      state: {
        fromDate,
        toDate,
      },
    });
  };

  return (
    <div className="write-page">
      <h2 className="write-title">View Notes</h2>

      {/* ================= DATE ROW (HORIZONTAL) ================= */}
      <div className="date-row">
        <div className="date-field">
          <label>From :</label>
          <DatePicker
            selected={fromDate}
            onChange={(date) => setFromDate(date)}
            dateFormat="dd/MM/yyyy"
            className="calendar-input"
            placeholderText="Select start date"
            showPopperArrow={false}
          />
        </div>

        <div className="date-field">
          <label>To :</label>
          <DatePicker
            selected={toDate}
            onChange={(date) => setToDate(date)}
            dateFormat="dd/MM/yyyy"
            className="calendar-input"
            placeholderText="Select end date"
            minDate={fromDate}
            showPopperArrow={false}
          />
        </div>
      </div>

      {/* ================= ACTION BUTTONS ================= */}
      <div className="write-actions">
        <button className="btn-back" onClick={() => navigate(-1)}>
          Back
        </button>

        <button className="btn-save" onClick={handleView}>
          View
        </button>
      </div>
    </div>
  );
}
