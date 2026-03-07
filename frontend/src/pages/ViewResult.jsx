import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "../App.css";

export default function ViewResult() {

  const navigate = useNavigate();
  const { state } = useLocation();

  const fromDate = state?.fromDate;
  const toDate = state?.toDate;

  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(false);


  // =========================
  // Format Date (Fix timezone bug)
  // =========================
  const formatDate = (date) => {

    const d = new Date(date);

    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  };


  // =========================
  // Load Data when Date Changes
  // =========================
  useEffect(() => {

    if (!fromDate || !toDate) return;

    fetchNotes();

  }, [fromDate, toDate]);


  // =========================
  // Fetch Notes
  // =========================
  const fetchNotes = async () => {

    try {

      setLoading(true);

      const start = formatDate(fromDate);
      const end = formatDate(toDate);

      console.log("Fetching:", start, end); // Debug

      const res = await fetch(
        `http://127.0.0.1:8000/notes-by-date?from_date=${start}&to_date=${end}`,
        {
          cache: "no-store"   // ❗ Prevent cache issue
        }
      );

      if (!res.ok) {
        throw new Error("API Error");
      }

      const data = await res.json();

      console.log("Result:", data); // Debug

      setNotes(data);

    } catch (err) {

      console.error(err);
      alert("Failed to load data");

    } finally {

      setLoading(false);
    }
  };


  // =========================
  // Delete Note
  // =========================
  const handleDelete = async (id) => {

    if (!window.confirm("Are you sure you want to delete?")) return;

    try {

      const res = await fetch(
        `http://127.0.0.1:8000/notes/${id}`,
        {
          method: "DELETE"
        }
      );

      if (res.ok) {

        alert("Deleted Successfully");
        fetchNotes();

      } else {

        alert("Delete Failed");
      }

    } catch (err) {

      alert("Server Error");
    }
  };


  // =========================
  // UI
  // =========================
  return (

    <div className="write-page wide-page">


      {/* Title */}
      <h2 className="write-title">Teachers Notes</h2>


      {/* Date Range */}
      <p>
        <strong>From:</strong>{" "}
        {fromDate ? new Date(fromDate).toDateString() : "-"} <br />

        <strong>To:</strong>{" "}
        {toDate ? new Date(toDate).toDateString() : "-"}
      </p>


      {/* Loading */}
      {loading && <p>Loading...</p>}


      {/* No Data */}
      {!loading && notes.length === 0 && (
        <p>No data found.</p>
      )}


      {/* Table */}
      {!loading && notes.length > 0 && (

        <div className="table-wrapper-full">

          <table className="teacher-table-full">


            <thead>
              <tr>

                <th>Date</th>
                <th>Name</th>
                <th>Prepared</th>
                <th>Did Well</th>
                <th>Went Well</th>
                <th>Improve</th>
                <th>Homework</th>
                <th>Action</th>

              </tr>
            </thead>


            <tbody>

              {notes.map((n) => (

                <tr key={n.id}>


                  <td>{n.created_date}</td>

                  <td>{n.username}</td>

                  <td>{n.what_i_prepared}</td>

                  <td>{n.what_i_did_well}</td>

                  <td>{n.what_went_well}</td>

                  <td>{n.where_to_improve}</td>

                  <td>{n.what_homework_did_i_give}</td>


                  {/* Buttons */}
                  <td className="action-col">


                    <button
                      className="btn-edit"
                      onClick={() => navigate(`/edit/${n.id}`)}
                    >
                      Edit
                    </button>


                    <button
                      className="btn-delete"
                      onClick={() => handleDelete(n.id)}
                    >
                      Delete
                    </button>


                  </td>

                </tr>

              ))}

            </tbody>


          </table>

        </div>

      )}


      {/* Back */}
      <button
        className="btn-back"
        onClick={() => navigate(-1)}
      >
        Back
      </button>


    </div>
  );
}
