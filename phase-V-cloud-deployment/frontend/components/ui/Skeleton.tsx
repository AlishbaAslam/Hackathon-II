interface SkeletonProps {
  className?: string;
  width?: string;
  height?: string;
  circle?: boolean;
}

export default function Skeleton({ className = '', width, height, circle }: SkeletonProps) {
  const style = {
    width: width || '100%',
    height: height || '1rem',
    borderRadius: circle ? '50%' : '0.375rem', // rounded-md
  };

  return (
    <div
      className={`animate-pulse bg-gray-200 ${className}`}
      style={style}
    />
  );
}

// Common skeleton components for typical UI elements
export const SkeletonCard = () => (
  <div className="p-4 bg-white rounded-lg shadow">
    <Skeleton className="mb-4" height="1.5rem" width="60%" />
    <Skeleton className="mb-2" height="1rem" />
    <Skeleton className="mb-2" height="1rem" width="80%" />
    <Skeleton height="0.75rem" width="40%" />
  </div>
);

export const SkeletonList = ({ count = 3 }) => (
  <div className="space-y-4">
    {Array.from({ length: count }).map((_, index) => (
      <div key={index} className="flex items-center space-x-4">
        <Skeleton circle height="2.5rem" width="2.5rem" />
        <div className="flex-1 space-y-2">
          <Skeleton height="1rem" width="60%" />
          <Skeleton height="0.75rem" width="40%" />
        </div>
      </div>
    ))}
  </div>
);

export const SkeletonButton = () => (
  <Skeleton width="8rem" height="2.5rem" />
);