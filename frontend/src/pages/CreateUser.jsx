import axios from "axios";
import { useState } from "react";
import { FaSchool } from "react-icons/fa";

export default function CreateUser() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    full_name: "",
    phonenumber: "",
    school:"",
    grade:"",
    photo: null,
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    if (name === "photo") {
      setForm({ ...form, photo: files[0] });
    } else {
      setForm({ ...form, [name]: value });
    }
  };

  const submit = async () => {
    try {
      setLoading(true);

      const token = localStorage.getItem("token");

      if (!token) {
        alert("Admin not logged in");
        return;
      }

      const data = new FormData();

      data.append("username", form.username);
      data.append("email", form.email);
      data.append("password", form.password);
      data.append("full_name", form.full_name);
      data.append("phonenumber", form.phonenumber);
      data.append("school", form.school);
      data.append("grade", form.grade);

      if (form.photo) {
        data.append("photo", form.photo);
      }

      await axios.post(
        "http://localhost:8000/users/create",
        data,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert("User created successfully");

      // Reset form
      setForm({
        username: "",
        email: "",
        password: "",
        full_name: "",
        phonenumber: "",
        photo: null,
      });

    } catch (err) {
      console.error("Server Error:", err.response?.data);
      alert(
        err.response?.data?.detail || 
        "Error creating user"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "30px", maxWidth: "400px" }}>
      <h2>Create User</h2>

      <input
        name="username"
        placeholder="Username"
        value={form.username}
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="email"
        placeholder="Email"
        value={form.email}
        onChange={handleChange}
      />

      <br /><br />

      <input
        type="password"
        name="password"
        placeholder="Password"
        value={form.password}
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="full_name"
        placeholder="Full Name"
        value={form.full_name}
        onChange={handleChange}
      />

      <br /><br />

      <input
        name="phonenumber"
        placeholder="Phone Number"
        value={form.phonenumber}
        onChange={handleChange}
      />

      <br /><br />

<select name="school" value={form.school} onChange={handleChange}>
  <option value="">Select School</option>
  <option value="AIAT">AIAT</option>
  <option value="UDAVI">UDAVI</option>
  <option value="ISAIAMBLAM">ISAIAMBLAM</option>
</select>

<br /><br />

<select name="grade" value={form.grade} onChange={handleChange}>
  <option value="">Select Grade</option>
  <option value="6">Grade 6</option>
  <option value="7">Grade 7</option>
  <option value="8">Grade 8</option>
  <option value="9">Grade 9</option>
  <option value="10">Grade 10</option>
  <option value="I-year">I-year</option>
   <option value="II-year">II-year</option>
    <option value="III-year">III-year</option>
</select>

      <br /><br />

      <input
        type="file"
        name="photo"
        onChange={handleChange}
      />

      <br /><br />

      <button onClick={submit} disabled={loading}>
        {loading ? "Creating..." : "Create User"}
      </button>
    </div>
  );
}