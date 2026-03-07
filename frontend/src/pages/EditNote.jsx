import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import "../App.css";

export default function EditNote() {

  const { id } = useParams(); // 👈 get ID from URL
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({
    username: "",
    school: "",
    grade: "",
    what_i_prepared: "",
    what_i_did_well: "",
    what_went_well: "",
    where_to_improve: "",
    created_date: "",
    user_id: "",
    what_homework_did_i_give: ""
  });


  // -------------------------------
  // Load Note Data
  // -------------------------------
  useEffect(() => {
    fetchNote();
  }, []);


  const fetchNote = async () => {

    try {

      const res = await fetch(`http://127.0.0.1:8000/notes/${id}`);
      const data = await res.json();

      setForm(data);

    } catch (err) {
      alert("Failed to load data");

    } finally {
      setLoading(false);
    }
  };


  // -------------------------------
  // Handle Input Change
  // -------------------------------
  const handleChange = (e) => {

    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };


  // -------------------------------
  // Save Changes
  // -------------------------------
  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      const res = await fetch(
        `http://127.0.0.1:8000/notes/${id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(form)
        }
      );

      if (res.ok) {

        alert("Updated Successfully ✅");
        navigate(-1); // go back

      } else {
        alert("Update Failed ❌");
      }

    } catch (err) {
      alert("Server Error");
    }
  };


  // -------------------------------
  // UI
  // -------------------------------
  if (loading) {
    return <p>Loading...</p>;
  }


  return (

    <div className="write-page">

      <h2 className="write-title">Edit Note</h2>


      <form onSubmit={handleSubmit} className="edit-form">


        <label>Date</label>
        <input
          type="date"
          name="created_date"
          value={form.created_date}
          onChange={handleChange}
        />


        <label>School</label>
        <input
          name="school"
          value={form.school}
          onChange={handleChange}
        />


        <label>Grade</label>
        <input
          name="grade"
          value={form.grade}
          onChange={handleChange}
        />


        <label>What I Prepared</label>
        <textarea
          name="what_i_prepared"
          value={form.what_i_prepared}
          onChange={handleChange}
        />


        <label>What I Did Well</label>
        <textarea
          name="what_i_did_well"
          value={form.what_i_did_well}
          onChange={handleChange}
        />


        <label>What Went Well</label>
        <textarea
          name="what_went_well"
          value={form.what_went_well}
          onChange={handleChange}
        />


        <label>Where To Improve</label>
        <textarea
          name="where_to_improve"
          value={form.where_to_improve}
          onChange={handleChange}
        />


        <label>Homework</label>
        <textarea
          name="what_homework_did_i_give"
          value={form.what_homework_did_i_give}
          onChange={handleChange}
        />


        {/* Buttons */}

        <div className="write-actions">

          <button
            type="button"
            className="btn-back"
            onClick={() => navigate(-1)}
          >
            Back
          </button>


          <button
            type="submit"
            className="btn-save"
          >
            Save Changes
          </button>

        </div>

      </form>

    </div>
  );
}
