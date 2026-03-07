import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../App.css";

export default function Write() {
  const navigate = useNavigate();

  const [selectedDate, setSelectedDate] = useState(new Date());

  const [form, setForm] = useState({
    school: "",
    grade: "",
    what_i_prepared: "",
    what_i_did_well: "",
    what_went_well: "",
    where_to_improve: "",
    what_homework_did_i_give: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSave = async () => {
    try {
      const token = localStorage.getItem("token");

      if (!token) {
        alert("Please login first");
        return;
      }

      const res = await fetch("http://localhost:8000/write", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...form,
          created_date: selectedDate.toISOString().split("T")[0],
          user_id: 1  // ideally fetch from backend later
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        console.error(errorData);
        throw new Error("Failed to save");
      }

      alert("Saved Successfully");
      navigate("/dashboard");

    } catch (err) {
      console.error(err);
      alert("Error saving note");
    }
  };

  return (
    <div className="write-page">
      <h2 className="write-title">Daily Reflection</h2>

      <div className="form-group">
        <label>Date</label>
        <DatePicker
          selected={selectedDate}
          onChange={(date) => setSelectedDate(date)}
          dateFormat="dd/MM/yyyy"
          className="calendar-input"
          showPopperArrow={false}
        />
      </div>

      <div className="form-group">
        <label>School</label>
        <input
          name="school"
          value={form.school}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>Grade</label>
        <input
          name="grade"
          value={form.grade}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>What I prepared</label>
        <textarea
          name="what_i_prepared"
          value={form.what_i_prepared}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>What I did well</label>
        <textarea
          name="what_i_did_well"
          value={form.what_i_did_well}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>What went well</label>
        <textarea
          name="what_went_well"
          value={form.what_went_well}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>Where to improve</label>
        <textarea
          name="where_to_improve"
          value={form.where_to_improve}
          onChange={handleChange}
        />
      </div>

      <div className="form-group">
        <label>What homework did I give today</label>
        <textarea
          name="what_homework_did_i_give"
          value={form.what_homework_did_i_give}
          onChange={handleChange}
        />
      </div>

      <div className="write-actions">
        <button className="btn-back" onClick={() => navigate(-1)}>
          Back
        </button>
        <button className="save-btn" onClick={handleSave}>
          Save
        </button>
      </div>
    </div>
  );
}