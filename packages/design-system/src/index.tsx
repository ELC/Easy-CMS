interface VersionBadgeProps {
  readonly label: string;
  readonly version: string;
}

export function VersionBadge({ label, version }: VersionBadgeProps) {
  return (
    <aside aria-label={label}>
      {label}: <strong>{version}</strong>
    </aside>
  );
}
