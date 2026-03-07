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
    photo: null,
    classes: [
    { school: "", grade: "" }
  ]
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

  const handleClassChange = (index, field, value) => {
  const updated = [...form.classes];
  updated[index][field] = value;

  setForm({
    ...form,
    classes: updated
  });
};

const addClass = () => {
  setForm({
    ...form,
    classes: [...form.classes, { school: "", grade: "" }]
  });
};

const removeClass = (index) => {
  const updated = form.classes.filter((_, i) => i !== index);

  setForm({
    ...form,
    classes: updated
  });
};

  const submit = async () => {
    try {
      setLoading(true);

      const token = localStorage.getItem("token");

      if (!token) {
        alert("Admin not logged in");
        return;
      }

      if (form.classes.some(c => !c.school || !c.grade)) {
      alert("Please select school and grade for all classes");
      return;
    }

      const data = new FormData();

      data.append("username", form.username);
      data.append("email", form.email);
      data.append("password", form.password);
      data.append("full_name", form.full_name);
      data.append("phonenumber", form.phonenumber);

      data.append("classes", JSON.stringify(form.classes));

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
        classes: [{ school: "", grade: "" }]
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

{form.classes.map((cls, index) => (
  <div key={index} style={{border:"1px solid #ccc", padding:"10px", marginBottom:"10px"}}>

    <select
      value={cls.school}
      onChange={(e) =>
        handleClassChange(index, "school", e.target.value)
      }
    >
      <option value="">Select School</option>
      <option value="AIAT">AIAT</option>
      <option value="UDAVI">UDAVI</option>
      <option value="ISAIAMBLAM">ISAIAMBLAM</option>
    </select>

    <br /><br />

    <select
      value={cls.grade}
      onChange={(e) =>
        handleClassChange(index, "grade", e.target.value)
      }
    >
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

    {index !== 0 && (
      <button onClick={() => removeClass(index)}>
        Remove
      </button>
    )}

  </div>
))}

<button onClick={addClass}>+ Add Another Class</button>
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