export default function WelcomeMessage() {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">
        Welcome to Todo AI Chatbot
      </h2>
      <p className="text-gray-600 mb-6 max-w-md">
        Manage your tasks by chatting with me. Try these commands:
      </p>
      <div className="space-y-2 text-left text-sm text-gray-500 max-w-md">
        <p className="flex items-center gap-2">
          <span className="text-lg">💬</span>
          <span>&quot;Add a task: Buy groceries&quot;</span>
        </p>
        <p className="flex items-center gap-2">
          <span className="text-lg">📋</span>
          <span>&quot;Show my tasks&quot;</span>
        </p>
        <p className="flex items-center gap-2">
          <span className="text-lg">✅</span>
          <span>&quot;Mark Buy groceries as done&quot;</span>
        </p>
        <p className="flex items-center gap-2">
          <span className="text-lg">✏️</span>
          <span>&quot;Update Buy groceries to Buy organic groceries&quot;</span>
        </p>
        <p className="flex items-center gap-2">
          <span className="text-lg">🗑️</span>
          <span>&quot;Delete Buy groceries&quot;</span>
        </p>
      </div>
    </div>
  );
}
