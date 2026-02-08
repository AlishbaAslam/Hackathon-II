'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';

export default function HomePage() {
  const { isAuthenticated, loading: isLoading } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-[--background-gradient-start] to-[--background-gradient-end]">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 max-w-7xl mx-auto">
        <div className="text-2xl font-bold bg-gradient-to-r from-[--color-primary] to-[--color-accent] bg-clip-text text-transparent">
          TodoFlow
        </div>
        <div className="flex items-center space-x-4">
          {isLoading ? ( 
            <div className="h-4 w-20 bg-gray-200 rounded animate-pulse"></div>
          ) : isAuthenticated ? (
            <Link
              href="/dashboard"
              className="px-4 py-2 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all shadow-md hover:shadow-[--glow-primary]"
            >
              Dashboard
            </Link>
          ) : (
            <>
              <Link
                href="/login"
                className="px-4 py-2 text-[--text-primary] hover:text-[--color-primary] transition-colors font-medium"
              >
                Sign In
              </Link>
              <Link
                href="/signup"
                className="px-4 py-2 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all shadow-md hover:shadow-[--glow-primary]"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="mb-8"
          >
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-[--text-primary] mb-6 leading-tight">
              Streamline Your
              <span className="block bg-gradient-to-r from-[--color-primary] via-[--color-accent] to-[--color-secondary] bg-clip-text text-transparent animate-gradient">
                Productivity
              </span>
            </h1>
            <p className="text-xl text-[--text-secondary] max-w-2xl mx-auto mb-10 leading-relaxed">
              A professional task management solution designed to help you organize and accomplish your goals with ease.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex flex-col sm:flex-row gap-6 justify-center mb-16"
          >
            {!isLoading && !isAuthenticated && ( 
              <>
                <Link
                  href="/signup"
                  className="px-8 py-4 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-xl font-semibold text-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all transform hover:scale-105 shadow-[--glow-card] hover:shadow-[--glow-primary]"
                >
                  Start Free Trial
                </Link>
                <Link
                  href="/login"
                  className="px-8 py-4 bg-white text-[--text-primary] rounded-xl font-semibold text-lg border border-[--border-light] hover:border-[--color-primary] transition-all hover:shadow-md"
                >
                  Sign In
                </Link>
              </>
            )}
            {isAuthenticated && (
              <Link
                href="/dashboard"
                className="px-8 py-4 bg-gradient-to-r from-[--color-primary] to-[--color-accent] text-white rounded-xl font-semibold text-lg hover:from-[--color-primary-dark] hover:to-[--color-accent] transition-all transform hover:scale-105 shadow-[--glow-card] hover:shadow-[--glow-primary]"
              >
                Go to Dashboard
              </Link>
            )}
          </motion.div>

          {/* Features Preview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto"
          >
            <div className="glass card-hover bg-white/80 backdrop-blur-lg p-8 rounded-2xl border border-white/20 transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-[--color-primary] to-[--color-accent] rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-[--glow-card]">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-[--text-primary] mb-3 text-center">Task Management</h3>
              <p className="text-[--text-secondary] text-center leading-relaxed">
                Organize your tasks with our intuitive, professional interface.
              </p>
            </div>

            <div className="glass card-hover bg-white/80 backdrop-blur-lg p-8 rounded-2xl border border-white/20 transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-[--color-accent] to-[--color-secondary] rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-[--glow-card]">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-[--text-primary] mb-3 text-center">Create & Update</h3>
              <p className="text-[--text-secondary] text-center leading-relaxed">
                Easily create new tasks and update existing ones with our intuitive interface.
              </p>
            </div>

            <div className="glass card-hover bg-white/80 backdrop-blur-lg p-8 rounded-2xl border border-white/20 transition-all duration-300">
              <div className="w-16 h-16 bg-gradient-to-br from-[--color-success] to-[--color-primary] rounded-2xl flex items-center justify-center mb-6 mx-auto shadow-[--glow-card]">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-[--text-primary] mb-3 text-center">Delete</h3>
              <p className="text-[--text-secondary] text-center leading-relaxed">
                Remove completed tasks efficiently with our delete functionality.
              </p>
            </div>
          </motion.div>
        </div>
      </div>

      {/* How It Works */}
      <div className="max-w-6xl mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-[--text-primary] mb-4">
            How TodoFlow Works
          </h2>
          <p className="text-[--text-secondary] text-lg max-w-2xl mx-auto leading-relaxed">
            A simple workflow that keeps you focused: capture tasks and ship the day.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="glass card-hover bg-white/80 backdrop-blur-lg p-8 rounded-2xl border border-white/20 transition-all duration-300"
          >
            <div className="text-sm font-semibold text-[--color-primary] tracking-wider mb-3">01</div>
            <h3 className="text-xl font-bold text-[--text-primary] mb-3">Sign in securely</h3>
            <p className="text-[--text-secondary] leading-relaxed">
              Create an account and access your tasks anywhere with a clean, distraction-free experience.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="glass card-hover bg-white/80 backdrop-blur-lg p-8 rounded-2xl border border-white/20 transition-all duration-300"
          >
            <div className="text-sm font-semibold text-[--color-accent] tracking-wider mb-3">02</div>
            <h3 className="text-xl font-bold text-[--text-primary] mb-3">Add & update tasks</h3>
            <p className="text-[--text-secondary] leading-relaxed">
              Capture work in seconds, then refine details without losing momentum.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="glass card-hover bg-white/80 backdrop-blur-lg p-8 rounded-2xl border border-white/20 transition-all duration-300"
          >
            <div className="text-sm font-semibold text-[--color-success] tracking-wider mb-3">03</div>
            <h3 className="text-xl font-bold text-[--text-primary] mb-3">Complete with confidence</h3>
            <p className="text-[--text-secondary] leading-relaxed">
              Mark items done, keep an accurate view of what remains, and stay on track day after day.
            </p>
          </motion.div>
        </div>
      </div>

      {/* Todo App Highlights */}
      <section className="relative py-20">
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-white/40 via-white/15 to-transparent" />

        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-[--text-primary]">
              Everything you need to stay on track
            </h2>
            <p className="text-[--text-secondary] text-lg mt-3 max-w-2xl mx-auto">
              A focused, secure todo app built for fast capture, easy organization, and reliable progress.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
              className="glass card-hover bg-white/75 backdrop-blur-xl p-8 rounded-2xl border border-white/30 ring-1 ring-black/5"
            >
              <div className="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wider bg-primary/10 text-primary">
                SECURE BY DEFAULT
              </div>
              <div className="text-xl md:text-2xl font-bold text-[--text-primary] mt-4 mb-2">
                Private tasks
              </div>
              <div className="text-[--text-secondary] leading-relaxed">
                Authentication + user isolation keep your list yours.
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.7 }}
              className="glass card-hover bg-white/75 backdrop-blur-xl p-8 rounded-2xl border border-white/30 ring-1 ring-black/5"
            >
              <div className="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wider bg-accent/10 text-accent">
                BUILT FOR SPEED
              </div>
              <div className="text-xl md:text-2xl font-bold text-[--text-primary] mt-4 mb-2">
                Full task control
              </div>
              <div className="text-[--text-secondary] leading-relaxed">
                Add, edit, complete, and delete tasks with minimal friction.
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              className="glass card-hover bg-white/75 backdrop-blur-xl p-8 rounded-2xl border border-white/30 ring-1 ring-black/5"
            >
              <div className="inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wider bg-success/10 text-success">
                WORKS ANYWHERE
              </div>
              <div className="text-xl md:text-2xl font-bold text-[--text-primary] mt-4 mb-2">
                Responsive UI
              </div>
              <div className="text-[--text-secondary] leading-relaxed">
                Clean layout that feels great on mobile, tablet, and desktop.
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <div className="bg-gradient-to-r from-[--color-primary] to-[--color-accent] py-20">
        <div className="max-w-4xl mx-auto text-center px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.9 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Transform Your Productivity?
            </h2>
            <p className="text-white text-xl mb-10 max-w-2xl mx-auto">
              Join thousands of professionals who have already streamlined their workflow with our SaaS solution.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href={isAuthenticated ? "/dashboard" : "/signup"}
                className="px-8 py-4 bg-white text-[--color-primary] rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg hover:shadow-[--glow-primary]"
              >
                {isAuthenticated ? "Go to Dashboard" : "Get Started Free"}
              </Link>
              <Link
                href="/#features"
                className="px-8 py-4 bg-transparent text-white border-2 border-white rounded-xl font-semibold text-lg hover:bg-white/10 transition-all"
              >
                Learn More
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}