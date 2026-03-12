"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn, signUp } from "@/lib/auth-client";

interface AuthFormProps {
  mode: "signin" | "signup";
}

export default function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [nameError, setNameError] = useState("");
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  function validateName() {
    if (mode === "signup" && !name.trim()) {
      setNameError("Name is required");
      return false;
    }
    setNameError("");
    return true;
  }

  function validateEmail() {
    if (!email.trim()) {
      setEmailError("Email is required");
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setEmailError("Please enter a valid email address");
      return false;
    }
    setEmailError("");
    return true;
  }

  function validatePassword() {
    if (password.length < 8) {
      setPasswordError("Password must be at least 8 characters");
      return false;
    }
    setPasswordError("");
    return true;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (mode === "signup") {
        const { error: signUpError } = await signUp.email({
          email,
          password,
          name,
        });
        if (signUpError) {
          setError(signUpError.message || "Sign up failed");
          return;
        }
        router.push("/signin");
      } else {
        const { error: signInError } = await signIn.email({
          email,
          password,
        });
        if (signInError) {
          setError(signInError.message || "Sign in failed");
          return;
        }
        window.location.href = "/dashboard";
      }
    } catch {
      setError("An unexpected error occurred");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-full max-w-sm">
      <h1 className="text-xl sm:text-2xl font-bold text-center">
        {mode === "signin" ? "Sign In" : "Sign Up"}
      </h1>

      {error && (
        <div role="alert" aria-live="assertive" className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded text-sm">
          {error}
        </div>
      )}

      {mode === "signup" && (
        <div className="flex flex-col gap-1">
          <label htmlFor="auth-name" className="text-sm font-medium text-gray-700">
            Name
          </label>
          <input
            id="auth-name"
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onBlur={validateName}
            required
            aria-invalid={!!nameError}
            aria-describedby={nameError ? "name-error" : undefined}
            className="border border-gray-300 rounded-lg px-4 py-2 min-h-[44px] focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {nameError && (
            <p id="name-error" role="alert" className="text-sm text-red-600">
              {nameError}
            </p>
          )}
        </div>
      )}

      <div className="flex flex-col gap-1">
        <label htmlFor="auth-email" className="text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="auth-email"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          onBlur={validateEmail}
          required
          aria-invalid={!!emailError}
          aria-describedby={emailError ? "email-error" : undefined}
          className="border border-gray-300 rounded-lg px-4 py-2 min-h-[44px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {emailError && (
          <p id="email-error" role="alert" className="text-sm text-red-600">
            {emailError}
          </p>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="auth-password" className="text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="auth-password"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onBlur={validatePassword}
          required
          minLength={8}
          aria-invalid={!!passwordError}
          aria-describedby={mode === "signup" ? "password-hint password-error" : passwordError ? "password-error" : undefined}
          className="border border-gray-300 rounded-lg px-4 py-2 min-h-[44px] focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {mode === "signup" && (
          <p id="password-hint" className="text-xs text-gray-500">
            Minimum 8 characters
          </p>
        )}
        {passwordError && (
          <p id="password-error" role="alert" className="text-sm text-red-600">
            {passwordError}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={loading}
        className="bg-blue-600 text-white rounded-lg px-4 py-2 min-h-[44px] font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        {loading
          ? "Loading..."
          : mode === "signin"
            ? "Sign In"
            : "Sign Up"}
      </button>

      <p className="text-center text-sm text-gray-600">
        {mode === "signin" ? (
          <>
            Don&apos;t have an account?{" "}
            <a href="/signup" className="text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded">
              Sign Up
            </a>
          </>
        ) : (
          <>
            Already have an account?{" "}
            <a href="/signin" className="text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded">
              Sign In
            </a>
          </>
        )}
      </p>
    </form>
  );
}
