// "use client";

// import React, { useState, useEffect, createContext, useContext, useRef, FormEvent } from 'react';

// // --- CONSTANTS ---
// const API_URL = "http://127.0.0.1:8000";

// // --- Authentication Context ---
// interface AuthContextType {
//     token: string | null;
//     setToken: (token: string | null) => void;
//     logout: () => void;
// }
// const AuthContext = createContext<AuthContextType | null>(null);

// const AuthProvider = ({ children }: { children: React.ReactNode }) => {
//     const [token, setToken] = useState<string | null>(null);

//     useEffect(() => {
//         const storedToken = localStorage.getItem('nivara_token');
//         if (storedToken) {
//             setToken(storedToken);
//         }
//     }, []);

//     const handleSetToken = (newToken: string | null) => {
//         setToken(newToken);
//         if (newToken) {
//             localStorage.setItem('nivara_token', newToken);
//         } else {
//             localStorage.removeItem('nivara_token');
//         }
//     };

//     const logout = () => {
//         handleSetToken(null);
//     };

//     return (
//         <AuthContext.Provider value={{ token, setToken: handleSetToken, logout }}>
//             {children}
//         </AuthContext.Provider>
//     );
// };

// const useAuth = () => {
//     const context = useContext(AuthContext);
//     if (!context) {
//         throw new Error('useAuth must be used within an AuthProvider');
//     }
//     return context;
// };

// // --- UI Components ---
// const Header = () => {
//     const { logout } = useAuth();
//     return (
//         <header className="relative flex items-center justify-between px-8 py-5 bg-gradient-to-r from-[#4A3F71] to-[#5E507F] z-10 shrink-0">
//             <div className="flex items-center relative">
//                 <div className="absolute -left-3 top-1/2 transform -translate-y-1/2 w-1.5 h-6 bg-teal-400 rounded-full opacity-80"></div>
//                 <span className="font-bold text-white text-xl tracking-tight">Nivara</span>
//             </div>
//             <button
//                 onClick={logout}
//                 className="text-white/80 text-xs px-4 py-2 font-medium hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200 cursor-pointer"
//             >
//                 LOGOUT
//             </button>
//         </header>
//     );
// }

// const TypingAnimation = () => (
//     <div className="flex items-center space-x-1.5 p-2">
//         <div className="w-1.5 h-1.5 bg-gray-400/70 rounded-full animate-pulse" style={{ animationDuration: "1s", animationDelay: "0ms" }}></div>
//         <div className="w-1.5 h-1.5 bg-gray-400/70 rounded-full animate-pulse" style={{ animationDuration: "1s", animationDelay: "300ms" }}></div>
//         <div className="w-1.5 h-1.5 bg-gray-400/70 rounded-full animate-pulse" style={{ animationDuration: "1s", animationDelay: "600ms" }}></div>
//     </div>
// );

// interface Message {
//     id: number;
//     content: string;
//     isUser: boolean;
//     isLoading?: boolean;
//     toolStatus?: string;
// }

// interface MessageAreaProps {
//   messages: Message[];
//   messagesEndRef: React.RefObject<HTMLDivElement | null>;
// }

// const MessageArea = ({ messages, messagesEndRef }: MessageAreaProps) => (
//     <div className="flex-grow overflow-y-auto bg-[#FCFCF8]" style={{ minHeight: 0 }}>
//         <div className="max-w-4xl mx-auto p-6">
//             {messages.map((message) => (
//                 <div key={message.id} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'} mb-5`}>
//                     <div className={`rounded-lg py-3 px-5 max-w-xl break-words whitespace-pre-wrap ${
//                         message.isUser
//                             ? 'bg-gradient-to-br from-[#5E507F] to-[#4A3F71] text-white rounded-br-none shadow-md'
//                             : 'bg-[#F3F3EE] text-gray-800 border border-gray-200 rounded-bl-none shadow-sm'
//                     }`}>
//                         {message.toolStatus && <div className="text-xs text-gray-500 italic pb-2 border-b border-gray-300 mb-2">{message.toolStatus}</div>}
//                         {message.isLoading && !message.content && !message.toolStatus ? <TypingAnimation /> : message.content}
//                     </div>
//                 </div>
//             ))}
//             <div ref={messagesEndRef} />
//         </div>
//     </div>
// );


// interface InputBarProps {
//   currentMessage: string;
//   setCurrentMessage: (value: string) => void;
//   onSubmit: (e: FormEvent) => void;
//   isStreaming: boolean;
// }

// const InputBar = ({ currentMessage, setCurrentMessage, onSubmit, isStreaming }: InputBarProps) => (
//     <form onSubmit={onSubmit} className="p-4 bg-white border-t border-gray-200 shrink-0">
//         <div className="flex items-center bg-[#F9F9F5] rounded-full p-3 shadow-md border border-gray-200">
//             <input
//                 type="text"
//                 placeholder="Type a message..."
//                 value={currentMessage}
//                 onChange={(e) => setCurrentMessage(e.target.value)}
//                 disabled={isStreaming}
//                 className="flex-grow px-4 py-2 bg-transparent focus:outline-none text-gray-700 disabled:opacity-50"
//             />
//             <button
//                 type="submit"
//                 disabled={isStreaming || !currentMessage.trim()}
//                 className="bg-gradient-to-r from-teal-500 to-teal-400 hover:from-teal-600 hover:to-teal-500 rounded-full p-3 ml-2 shadow-md transition-all duration-200 group disabled:opacity-50 disabled:cursor-not-allowed"
//             >
//                 <svg className="w-6 h-6 text-white transform -rotate-45 group-hover:scale-110 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
//             </button>
//         </div>
//     </form>
// );


// // --- Page Components ---

// const ChatPage = () => {
//     const { token } = useAuth();
//     const [messages, setMessages] = useState<Message[]>([
//         { id: Date.now(), content: 'Hello! I am Nivara, your AI financial companion. How can I help you today?', isUser: false }
//     ]);
//     const [currentMessage, setCurrentMessage] = useState("");
//     const [isStreaming, setIsStreaming] = useState(false);
//     const messagesEndRef = useRef<HTMLDivElement | null>(null);

//     useEffect(() => {
//         messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//     }, [messages]);

//     const handleSubmit = async (e: FormEvent) => {
//         e.preventDefault();
//         if (!currentMessage.trim() || isStreaming || !token) return;

//         setIsStreaming(true);
//         const userMessageContent = currentMessage;
        
//         // **FIX**: Create both new message objects first with unique IDs
//         const userMessage: Message = { 
//             id: Date.now(), 
//             content: userMessageContent, 
//             isUser: true 
//         };
//         const aiResponsePlaceholder: Message = { 
//             id: userMessage.id + 1, // Ensure unique ID
//             content: "", 
//             isUser: false, 
//             isLoading: true 
//         };

//         // **FIX**: Update state only once with both new messages
//         setMessages(prev => [...prev, userMessage, aiResponsePlaceholder]);
//         setCurrentMessage("");

//         try {
//             const response = await fetch(`${API_URL}/chat-stream`, {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'Authorization': `Bearer ${token}`
//                 },
//                 body: JSON.stringify({ message: userMessageContent }),
//             });

//             if (!response.body) return;
//             const reader = response.body.getReader();
//             const decoder = new TextDecoder();
//             let streamedContent = "";

//             while (true) {
//                 const { done, value } = await reader.read();
//                 if (done) break;
                
//                 const chunk = decoder.decode(value, { stream: true });
//                 const lines = chunk.split('\n\n').filter(line => line.trim());

//                 for (const line of lines) {
//                     if (line.startsWith('data: ')) {
//                         const jsonStr = line.substring(6);
//                         try {
//                             const data = JSON.parse(jsonStr);
//                             const aiResponseId = aiResponsePlaceholder.id;

//                             if (data.type === 'tool_start') {
//                                 setMessages(prev => prev.map(msg => msg.id === aiResponseId ? { ...msg, toolStatus: data.content, content: streamedContent } : msg));
//                             } else if (data.type === 'tool_end') {
//                                 setMessages(prev => prev.map(msg => msg.id === aiResponseId ? { ...msg, toolStatus: undefined, content: streamedContent } : msg));
//                             } else if (data.type === 'content') {
//                                 streamedContent += data.content;
//                                 setMessages(prev => prev.map(msg => msg.id === aiResponseId ? { ...msg, content: streamedContent, isLoading: true } : msg));
//                             } else if (data.type === 'end') {
//                                 setMessages(prev => prev.map(msg => msg.id === aiResponseId ? { ...msg, isLoading: false } : msg));
//                                 setIsStreaming(false);
//                                 return;
//                             }
//                         } catch (e) { console.error("Error parsing JSON:", e, jsonStr); }
//                     }
//                 }
//             }
//         } catch (error: unknown) {
//             console.error("Fetch error:", error);
//             let errorMessage = "Sorry, an error occurred while connecting to the server.";
//             if (error instanceof Error) {
//                 errorMessage = error.message;
//             }
//             setMessages(prev => prev.map(msg => msg.id === aiResponsePlaceholder.id ? { ...msg, content: errorMessage, isLoading: false } : msg));
//         } finally {
//             setIsStreaming(false);
//         }
//     };

//     return (
//         <div className="w-full max-w-4xl bg-white flex flex-col rounded-xl shadow-lg border border-gray-100 overflow-hidden h-[90vh]">
//             <Header />
//             <MessageArea messages={messages} messagesEndRef={messagesEndRef} />
//             <InputBar currentMessage={currentMessage} setCurrentMessage={setCurrentMessage} onSubmit={handleSubmit} isStreaming={isStreaming} />
//         </div>
//     );
// };

// const AuthPage = () => {
//     const { setToken } = useAuth();
//     const [email, setEmail] = useState('');
//     const [password, setPassword] = useState('');
//     const [isLogin, setIsLogin] = useState(true);
//     const [error, setError] = useState('');
//     const [loading, setLoading] = useState(false);
    
//     const handleAuth = async (e: FormEvent) => {
//         e.preventDefault();
//         setError('');
//         setLoading(true);
//         const url = `${API_URL}/${isLogin ? 'login' : 'signup'}`;
//         const headers = isLogin ? { 'Content-Type': 'application/x-www-form-urlencoded' } : { 'Content-Type': 'application/json' };
//         const body = isLogin ? new URLSearchParams({ username: email, password: password }) : JSON.stringify({ email, password });
        
//         try {
//             const response = await fetch(url, {
//                 method: 'POST',
//                 headers,
//                 body: body.toString(),
//             });

//             const data = await response.json();
//             if (!response.ok) {
//                 throw new Error(data.detail || 'Authentication failed');
//             }
//             setToken(data.access_token);
//         } catch (err: unknown) {
//             if (err instanceof Error) {
//                 setError(err.message);
//             } else {
//                 setError('An unknown error occurred.');
//             }
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="w-full max-w-md mx-auto p-8 bg-white rounded-xl shadow-lg border border-gray-200">
//             <h2 className="text-3xl font-bold text-center text-gray-800 mb-2">{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
//             <p className="text-center text-gray-500 mb-8">{isLogin ? 'Login to your Nivara account' : 'Create your free Nivara account'}</p>
//             <form onSubmit={handleAuth}>
//                 <input
//                     type="email"
//                     value={email}
//                     onChange={(e) => setEmail(e.target.value)}
//                     placeholder="Email Address"
//                     required
//                     className="w-full px-4 py-3 mb-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 transition-all"
//                 />
//                 <input
//                     type="password"
//                     value={password}
//                     onChange={(e) => setPassword(e.target.value)}
//                     placeholder="Password"
//                     required
//                     minLength={6}
//                     className="w-full px-4 py-3 mb-6 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500 transition-all"
//                 />
//                 {error && <p className="text-red-500 text-sm mb-4 text-center">{error}</p>}
//                 <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-teal-500 to-teal-400 text-white py-3 rounded-lg font-semibold hover:from-teal-600 hover:to-teal-500 transition-all duration-200 disabled:opacity-50">
//                     {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
//                 </button>
//             </form>
//             <p className="text-center text-sm text-gray-600 mt-6">
//                 {isLogin ? "Don't have an account?" : "Already have an account?"}
//                 <button onClick={() => { setIsLogin(!isLogin); setError(''); }} className="text-teal-500 hover:text-teal-600 font-semibold ml-1">
//                     {isLogin ? 'Sign Up' : 'Login'}
//                 </button>
//             </p>
//         </div>
//     );
// };

// // --- Main App Component ---
// export default function Home() {
//     return (
//         <AuthProvider>
//             <main className="flex justify-center items-center bg-gray-100 min-h-screen py-8 px-4">
//                 <AppContent />
//             </main>
//         </AuthProvider>
//     );
// }

// const AppContent = () => {
//     const { token } = useAuth();
//     const [isAuthReady, setIsAuthReady] = useState(false);
//     useEffect(() => {
//         setIsAuthReady(true);
//     }, []);

//     if (!isAuthReady) {
//         return null; // Or a loading spinner
//     }

//     return token ? <ChatPage /> : <AuthPage />;
// };

"use client";

import React, { useState, useEffect, createContext, useContext, useRef, FormEvent } from 'react';

// --- CONSTANTS ---
const API_URL = "http://127.0.0.1:8000";

// --- SVG ICONS ---
const PlusIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 5V19M5 12H19" stroke="#E2E2E2" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
);
const ToolsIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M14.2426 18.841L18.841 14.2426M11.8198 14.384L12.3604 14.9246C13.2598 15.8239 14.6787 15.8239 15.5781 14.9246V14.9246C16.4775 14.0252 16.4775 12.6063 15.5781 11.7069L11.7069 7.82845C10.8075 6.92909 9.38857 6.92909 8.48921 7.82845V7.82845C7.58985 8.72781 7.58985 10.1467 8.48921 11.0461L9.03099 11.5879M9.61601 20.3839L12.4121 17.5879M3 12.8787L6.87868 9M3.61601 3.61601L5.12132 5.12132" stroke="#E2E2E2" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
);
const MicIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 18.5C14.4853 18.5 16.5 16.4853 16.5 14V6C16.5 3.51472 14.4853 1.5 12 1.5C9.51472 1.5 7.5 3.51472 7.5 6V14C7.5 16.4853 9.51472 18.5 12 18.5Z" stroke="#E2E2E2" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M20 11V14C20 18.4183 16.4183 22 12 22C7.58172 22 4 18.4183 4 14V11" stroke="#E2E2E2" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
);

// --- TYPE DEFINITIONS ---
interface AuthContextType {
    token: string | null;
    setToken: (token: string | null) => void;
    logout: () => void;
    userName: string;
}
interface Message { 
    id: number; 
    content: string; 
    isUser: boolean; 
    isLoading?: boolean; 
    toolStatus?: string; 
}
interface InputBarProps {
  currentMessage: string;
  setCurrentMessage: (value: string) => void;
  onSubmit: (e: FormEvent) => void;
  isStreaming: boolean;
}

// --- Authentication Context ---
const AuthContext = createContext<AuthContextType | null>(null);

const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [token, setToken] = useState<string | null>(null);
    const [userName, setUserName] = useState("User");

    const logout = React.useCallback(() => {
        setToken(null);
        localStorage.removeItem('nivara_token');
        setUserName("User");
    }, []);

    useEffect(() => {
        const storedToken = localStorage.getItem('nivara_token');
        if (storedToken) {
            setToken(storedToken);
            try {
                const payload = JSON.parse(atob(storedToken.split('.')[1]));
                const name = payload.sub.split('@')[0];
                const capitalizedName = name.charAt(0).toUpperCase() + name.slice(1);
                setUserName(capitalizedName);
            } catch (e) {
                console.error("Failed to parse token:", e);
                logout();
            }
        }
    }, [logout]);

    const handleSetToken = (newToken: string | null) => {
        setToken(newToken);
        if (newToken) {
            localStorage.setItem('nivara_token', newToken);
             try {
                const payload = JSON.parse(atob(newToken.split('.')[1]));
                const name = payload.sub.split('@')[0];
                const capitalizedName = name.charAt(0).toUpperCase() + name.slice(1);
                setUserName(capitalizedName);
            } catch (e) {
                console.error("Failed to parse new token:", e);
            }
        } else {
            logout();
        }
    };

    return (
        <AuthContext.Provider value={{ token, setToken: handleSetToken, logout, userName }}>
            {children}
        </AuthContext.Provider>
    );
};

const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within an AuthProvider');
    return context;
};

// --- Gemini Style UI Components ---
const GeminiHeader = () => {
    const { userName, logout } = useAuth();
    const userInitial = userName ? userName.charAt(0).toUpperCase() : 'U';
    return (
        <header className="absolute top-0 left-0 right-0 flex items-center justify-between p-4 z-10 w-full">
            <div className="flex items-center space-x-2">
                 <span className="font-semibold text-lg text-gray-300">Nivara</span>
                 <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-400"><path d="M6 9L12 15L18 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
            </div>
            <div className="flex items-center space-x-4">
                 <button onClick={logout} className="text-sm text-gray-300 hover:text-white transition-colors">Logout</button>
                 <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-bold">
                     {userInitial}
                 </div>
            </div>
        </header>
    );
}

const GeminiInputBar = ({ currentMessage, setCurrentMessage, onSubmit, isStreaming }: InputBarProps) => (
    <form onSubmit={onSubmit} className="w-full max-w-4xl p-4">
        <div className="relative">
            <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                disabled={isStreaming}
                placeholder="Ask Nivara"
                className="w-full bg-[#1E1F20] border border-gray-600/50 rounded-full h-16 pl-6 pr-40 text-gray-200 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
            />
            <div className="absolute inset-y-0 right-0 flex items-center pr-4 space-x-2">
                <button type="button" className="p-2 rounded-full hover:bg-gray-700 transition-colors"><PlusIcon /></button>
                <button type="button" className="p-2 rounded-full hover:bg-gray-700 transition-colors"><ToolsIcon /></button>
                <button type="submit" disabled={isStreaming || !currentMessage.trim()} className="p-2 rounded-full hover:bg-gray-700 disabled:opacity-50 transition-colors"><MicIcon /></button>
            </div>
        </div>
    </form>
);

const TypingAnimation = () => (
    <div className="flex items-center space-x-1.5 p-2">
        {[0, 1, 2].map(i => <div key={i} className="w-1.5 h-1.5 bg-gray-400/70 rounded-full animate-pulse" style={{ animationDuration: "1s", animationDelay: `${i * 300}ms` }}></div>)}
    </div>
);

const GeminiMessageArea = ({ messages, messagesEndRef }: { messages: Message[], messagesEndRef: React.RefObject<HTMLDivElement | null> }) => {
    const { userName } = useAuth();
    
    return (
        <div className="flex-grow w-full max-w-4xl overflow-y-auto px-4 pt-20 pb-10">
            {messages.map((message) => (
                <div key={message.id} className={`flex flex-col items-start ${message.isUser ? 'items-end' : ''} mb-6`}>
                     <div className={`text-sm font-bold mb-2 ${message.isUser ? "text-blue-400" : "text-gray-300"}`}>
                        {message.isUser ? userName : "Nivara"}
                     </div>
                    <div className={`py-3 px-5 max-w-xl break-words whitespace-pre-wrap rounded-2xl ${
                        message.isUser 
                            ? 'bg-gradient-to-br from-blue-600 to-purple-600 text-white' 
                            : 'bg-[#1E1F20] text-gray-200'
                    }`}>
                        {message.toolStatus && <div className="text-xs text-gray-400 italic pb-2 border-b border-gray-600 mb-2">{message.toolStatus}</div>}
                        {message.isLoading && !message.content && !message.toolStatus ? <TypingAnimation /> : message.content}
                    </div>
                </div>
            ))}
            <div ref={messagesEndRef} />
        </div>
    );
};

// --- Page Components ---
const ChatPage = () => {
    const { token, userName } = useAuth();
    const [messages, setMessages] = useState<Message[]>([]);
    const [currentMessage, setCurrentMessage] = useState("");
    const [isStreaming, setIsStreaming] = useState(false);
    const [conversationStarted, setConversationStarted] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        if (!currentMessage.trim() || isStreaming || !token) return;
        
        if (!conversationStarted) {
            setConversationStarted(true);
        }

        setIsStreaming(true);
        const userMessageContent = currentMessage;
        const userMessage: Message = { id: Date.now(), content: userMessageContent, isUser: true };
        const aiResponsePlaceholder: Message = { id: userMessage.id + 1, content: "", isUser: false, isLoading: true };

        setMessages(prev => [...prev, userMessage, aiResponsePlaceholder]);
        setCurrentMessage("");

        try {
            const response = await fetch(`${API_URL}/chat-stream`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`},
                body: JSON.stringify({ message: userMessageContent }),
            });

            if (!response.body) return;
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let streamedContent = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value, { stream: true });
                const lines = chunk.split('\n\n').filter(line => line.trim());

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const jsonStr = line.substring(6);
                        try {
                            const data = JSON.parse(jsonStr);
                            if (data.type === 'content') {
                                streamedContent += data.content;
                                setMessages(prev => prev.map(msg => msg.id === aiResponsePlaceholder.id ? { ...msg, content: streamedContent, isLoading: true } : msg));
                            } else if (data.type === 'end') {
                                setMessages(prev => prev.map(msg => msg.id === aiResponsePlaceholder.id ? { ...msg, isLoading: false } : msg));
                                setIsStreaming(false);
                                return;
                            }
                        } catch (e) { console.error("Error parsing JSON:", e, jsonStr); }
                    }
                }
            }
        } catch (error) {
            console.error("Fetch error:", error);
        } finally {
            setIsStreaming(false);
            setMessages(prev => prev.map(msg => msg.id === aiResponsePlaceholder.id ? { ...msg, isLoading: false } : msg));
        }
    };
    
    // **FIX**: Conditional rendering logic moved inside the return statement for clarity
    return (
        <div className="w-full h-full flex flex-col items-center bg-[#131314] text-white relative">
            <GeminiHeader />
            
            {!conversationStarted ? (
                // Initial State: "Hello" and Input Bar are centered together
                <div className="flex-grow flex flex-col items-center justify-center w-full">
                    <div className="flex flex-col items-center text-center px-4 mb-8">
                        <h1 className="text-5xl md:text-6xl font-medium bg-gradient-to-r from-blue-400 to-purple-400 text-transparent bg-clip-text mb-4">
                            Hello, {userName}
                        </h1>
                        <p className="text-gray-400 text-lg">How can I help you today?</p>
                    </div>
                    <GeminiInputBar 
                        currentMessage={currentMessage}
                        setCurrentMessage={setCurrentMessage}
                        onSubmit={handleSubmit}
                        isStreaming={isStreaming}
                    />
                </div>
            ) : (
                // Active Chat State: Messages fill space, Input Bar is at the bottom
                <>
                    <GeminiMessageArea messages={messages} messagesEndRef={messagesEndRef} />
                    <div className="w-full flex-shrink-0 flex justify-center">
                        <GeminiInputBar 
                            currentMessage={currentMessage}
                            setCurrentMessage={setCurrentMessage}
                            onSubmit={handleSubmit}
                            isStreaming={isStreaming}
                        />
                    </div>
                </>
            )}
        </div>
    );
};

const AuthPage = () => {
    const { setToken } = useAuth();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    const handleAuth = async (e: FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        const url = `${API_URL}/${isLogin ? 'login' : 'signup'}`;
        const headers = isLogin ? { 'Content-Type': 'application/x-www-form-urlencoded' } : { 'Content-Type': 'application/json' };
        const body = isLogin ? new URLSearchParams({ username: email, password: password }) : JSON.stringify({ email, password });
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers,
                body: body.toString(),
            });

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || 'Authentication failed');
            }
            setToken(data.access_token);
        } catch (err: unknown) {
            if (err instanceof Error) {
                setError(err.message);
            } else {
                setError('An unknown error occurred.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="w-full max-w-md mx-auto p-8 bg-[#1E1F20] rounded-2xl shadow-lg border border-gray-700 text-white">
            <h2 className="text-3xl font-bold text-center text-gray-200 mb-2">{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
            <p className="text-center text-gray-400 mb-8">Login to your Nivara account</p>
            <form onSubmit={handleAuth}>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email Address"
                    required
                    className="w-full px-4 py-3 mb-4 bg-[#2f3031] border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                    minLength={6}
                    className="w-full px-4 py-3 mb-6 bg-[#2f3031] border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                />
                {error && <p className="text-red-400 text-sm mb-4 text-center">{error}</p>}
                <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-600 transition-all duration-200 disabled:opacity-50">
                    {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
                </button>
            </form>
            <p className="text-center text-sm text-gray-400 mt-6">
                {isLogin ? "Don't have an account?" : "Already have an account?"}
                <button onClick={() => { setIsLogin(!isLogin); setError(''); }} className="text-blue-400 hover:text-blue-300 font-semibold ml-1">
                    {isLogin ? 'Sign Up' : 'Login'}
                </button>
            </p>
        </div>
    );
};

// --- Main App Component ---
export default function Home() {
    return (
        <AuthProvider>
            <main className="flex justify-center items-center bg-[#131314] min-h-screen h-screen">
                <AppContent />
            </main>
        </AuthProvider>
    );
}

const AppContent = () => {
    const { token } = useAuth();
    const [isAuthReady, setIsAuthReady] = useState(false);
    
    useEffect(() => {
        setIsAuthReady(true);
    }, []);

    if (!isAuthReady) {
        return null;
    }

    return (
        <div className="w-full h-full flex justify-center items-center">
            {token ? <ChatPage /> : <AuthPage />}
        </div>
    );
};




