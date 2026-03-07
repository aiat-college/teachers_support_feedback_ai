import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "../App.css";

export default function Write() {
  const navigate = useNavigate();

  const [date, setDate] = useState(new Date());
  const [prepared, setPrepared] = useState("");
  const [didWell, setDidWell] = useState("");
  const [wentWell, setWentWell] = useState("");
  const [improve, setImprove] = useState("");
  const [homework, setHomework] = useState("");

  // SAVE DATA
  const handleSave = async () => {
    const data = {
      username: "Navanith",
      school: "AIAT",
      grade: "9th",

      what_i_prepared: prepared,
      what_i_did_well: didWell,
      what_went_well: wentWell,
      where_to_improve: improve,

      created_date: date.toISOString().split("T")[0],
      user_id: 1,

      what_homework_did_i_give: homework
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/save", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      alert(result.message);

      navigate("/dashboard");

    } catch (err) {
      console.log(err);
      alert("Error saving data");
    }
  };

  return (
    <div className="write-page">

      <h2 className="write-title">Daily Reflection</h2>

      {/* Date */}
      <div className="form-group">
        <label>Date</label>

        <DatePicker
          selected={date}
          onChange={(d) => setDate(d)}
          dateFormat="dd/MM/yyyy"
          className="calendar-input"
        />
      </div>

      {/* Prepared */}
      <div className="form-group">
        <label>What I prepared</label>

        <textarea
          value={prepared}
          onChange={(e) => setPrepared(e.target.value)}
        />
      </div>

      {/* Did Well */}
      <div className="form-group">
        <label>What I did well</label>

        <textarea
          value={didWell}
          onChange={(e) => setDidWell(e.target.value)}
        />
      </div>

      {/* Went Well */}
      <div className="form-group">
        <label>What went well</label>

        <textarea
          value={wentWell}
          onChange={(e) => setWentWell(e.target.value)}
        />
      </div>

      {/* Improve */}
      <div className="form-group">
        <label>Where to improve</label>

        <textarea
          value={improve}
          onChange={(e) => setImprove(e.target.value)}
        />
      </div>

      {/* Homework */}
      <div className="form-group">
        <label>What homework did I give today</label>

        <textarea
          value={homework}
          onChange={(e) => setHomework(e.target.value)}
        />
      </div>

      {/* Buttons */}
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
