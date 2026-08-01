import { Outlet, Link } from 'react-router';
import { useAuth } from '../../context/AuthContext';

export function RootLayout() {
  const { logout, user } = useAuth();
  
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <header className="h-16 border-b flex items-center justify-between px-6 bg-white shrink-0">
        <h1 className="text-xl font-semibold text-primary">AI Business Analytics</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm font-medium text-gray-700">{user?.username}</span>
          <button 
            onClick={() => logout()} 
            className="text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>
      <div className="flex flex-1 overflow-hidden">
        <aside className="w-64 border-r bg-gray-50 p-4 hidden md:block">
          <nav className="space-y-2 flex flex-col">
            <Link to="/" className="text-sm font-medium text-gray-700 hover:text-primary p-2 rounded hover:bg-gray-100 transition-colors">Dashboard</Link>
            <Link to="/datasets" className="text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-primary p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">Datasets</Link>
            <Link to="/profile" className="text-sm font-medium text-gray-700 dark:text-gray-200 hover:text-primary p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">Profile</Link>
          </nav>
        </aside>
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
