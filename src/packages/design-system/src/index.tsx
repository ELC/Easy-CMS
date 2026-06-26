import "./version-badge.scss";

interface VersionBadgeProps {
  readonly label: string;
  readonly version: string;
}

export function VersionBadge({ label, version }: VersionBadgeProps) {
  return (
    <aside aria-label={label} className="version-badge">
      <span className="version-badge__label">{label}</span>
      <strong className="version-badge__value">{version}</strong>
    </aside>
  );
}
