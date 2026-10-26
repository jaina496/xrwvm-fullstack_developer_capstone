
import React, { useState } from "react";
import "./Register.css";
import Header from "../Header/Header";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const register = async (e) => {
    e.preventDefault();

    if (!userName.trim() || !password) {
      alert("Please enter a username and password.");
      return;
    }

    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch(
        window.location.origin + "/djangoapp/registration",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userName,
            password,
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        alert("Registration successful. Please log in.");
        window.location.href = "/login";
      } else {
        alert(data.error || "Registration failed.");
      }
    } catch (error) {
      console.error("Registration error:", error);
      alert("Could not connect to the server.");
    }
  };

  return (
    <div>
      <Header />

      <div className="register_container">
        <h1 className="header">Register</h1>

        <form onSubmit={register}>
          <div className="inputs">
            <div className="input">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                className="input_field"
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>

            <div className="input">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                className="input_field"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <div className="input">
              <label htmlFor="confirmPassword">Confirm password</label>
              <input
                id="confirmPassword"
                className="input_field"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="submit_panel">
            <button className="submit" type="submit">
              Register
            </button>
            <button
              className="submit"
              type="button"
              onClick={() => (window.location.href = "/login")}
            >
              Back to Login
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
