import { useState } from 'react';
import { useNavigate, Link } from 'react-router';
import { authApi } from '../services/auth_api';

export function Register() {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    try {
      await authApi.register({ email, username, password });
      navigate('/login');
    } catch (err: any) {
      if (err.response?.data?.message === "Validation Error" && err.response?.data?.data) {
        setError(err.response.data.data[0]?.msg || 'Validation failed');
      } else {
        setError(err.response?.data?.message || 'Failed to register');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
      <div className="w-full max-w-md space-y-8 bg-white p-8 shadow-sm rounded-lg border">
        <div>
          <h2 className="text-center text-3xl font-bold tracking-tight text-gray-900">Create an account</h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && <div className="text-red-500 text-sm text-center bg-red-50 p-2 rounded break-words">{error}</div>}
          <div className="space-y-4 rounded-md shadow-sm">
            <div>
              <input
                type="email"
                required
                className="relative block w-full rounded border-0 p-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-primary sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <input
                type="text"
                required
                className="relative block w-full rounded border-0 p-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-primary sm:text-sm"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div>
              <input
                type="password"
                required
                className="relative block w-full rounded border-0 p-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:z-10 focus:ring-2 focus:ring-primary sm:text-sm"
                placeholder="Password (min 12 chars, upper, lower, num, spec)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          <div>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex w-full justify-center rounded bg-primary px-3 py-3 text-sm font-semibold text-white hover:opacity-90 disabled:opacity-50"
            >
              {isSubmitting ? 'Creating account...' : 'Register'}
            </button>
          </div>
          <div className="text-sm text-center text-gray-500">
            Already have an account? <Link to="/login" className="font-semibold text-primary hover:underline">Log in</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
