import React from 'react';

class SectionErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, errorInfo) {
    console.error(`${this.props.title || 'Section'} failed to render`, error, errorInfo);
  }

  render() {
    if (this.state.error) {
      return (
        <section className="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-800 shadow-sm sm:p-6">
          <h2 className="text-lg font-semibold">{this.props.title || 'Section'} could not load</h2>
          <p className="mt-2">
            This panel failed to render, but the rest of the dashboard is still available.
            Check the browser console for details.
          </p>
          <pre className="mt-3 overflow-x-auto rounded bg-white/70 p-3 text-xs">
            {this.state.error.message}
          </pre>
        </section>
      );
    }

    return this.props.children;
  }
}

export default SectionErrorBoundary;
