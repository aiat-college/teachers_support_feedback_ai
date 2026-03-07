import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import "../App.css";

export default function ViewResult() {

  const navigate = useNavigate();
  const { state } = useLocation();

  const fromDate = state?.fromDate;
  const toDate = state?.toDate;

  const [notes, setNotes] = useState([]);

  useEffect(() => {

    if (!fromDate || !toDate) return;

    const fetchNotes = async () => {
      try {

        const token = localStorage.getItem("token");

        const res = await axios.get(
          `http://localhost:8000/notes-by-date?from_date=${fromDate}&to_date=${toDate}`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        setNotes(res.data);

      } catch (error) {
        console.log(error);
      }
    };

    fetchNotes();

  }, [fromDate, toDate]);


  const deleteNote = async (id) => {

    if(!window.confirm("Are you sure you want to delete this note?")) return;

    try {

      const token = localStorage.getItem("token");

      await axios.delete(`http://localhost:8000/notes/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      setNotes(notes.filter(note => note.id !== id));

    } catch (error) {
      console.log(error);
    }

  };


  return (
    <div className="write-page">

      <h2 className="write-title">Teachers Notes</h2>

      <p>
        <strong>From:</strong> {new Date(fromDate).toDateString()|| "-"} <br />
        <strong>To:</strong> {new Date(toDate).toDateString() || "-"}
      </p>

      <div className="table-wrapper">

        <table className="notes-table">

          <thead>
            <tr>
              <th>Date</th>
              <th>Prepared</th>
              <th>Did Well</th>
              <th>Went Well</th>
              <th>Improve</th>
              <th>Homework</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>

            {notes.length === 0 ? (
              <tr>
                <td colSpan="7">No records found</td>
              </tr>
            ) : (
              notes.map((note) => (
                <tr key={note.id}>
                  <td>{new Date(note.created_date).toDateString()}</td>
                  <td>{note.what_i_prepared}</td>
                  <td>{note.what_i_did_well}</td>
                  <td>{note.what_went_well}</td>
                  <td>{note.where_to_improve}</td>
                  <td>{note.what_homework_did_i_give}</td>

                  <td>
                    <button
                      className="table-btn edit"
                      onClick={() => navigate(`/edit/${note.id}`)}
                    >
                      Edit
                    </button>

                    <button
                      className="table-btn delete"
                      onClick={() => deleteNote(note.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}

          </tbody>

        </table>

      </div>

      <div className="write-actions">
        <button className="btn-back" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>

    </div>
  );
}