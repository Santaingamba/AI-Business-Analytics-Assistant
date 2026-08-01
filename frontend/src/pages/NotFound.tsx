import { Link } from 'react-router';

export function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-full space-y-4">
      <h2 className="text-4xl font-bold text-gray-800">404</h2>
      <p className="text-xl text-gray-600">Page not found</p>
      <Link to="/" className="text-primary hover:underline">
        Return to Home
      </Link>
    </div>
  );
}
