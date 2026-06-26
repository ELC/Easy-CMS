#!/usr/bin/env bash
set -euo pipefail

command_name="${1:-}"
package_name="${2:-}"

python_packages=(
  "sync-server-service"
  "studio-service"
  "python-shared"
)

browser_packages=(
  "sync-server-admin"
  "studio-web"
  "site-template"
  "design-system"
  "shared-types"
)

all_packages=(
  "${python_packages[@]}"
  "${browser_packages[@]}"
)

is_python_package() {
  local candidate="$1"
  for package in "${python_packages[@]}"; do
    [[ "$package" == "$candidate" ]] && return 0
  done
  return 1
}

is_browser_package() {
  local candidate="$1"
  for package in "${browser_packages[@]}"; do
    [[ "$package" == "$candidate" ]] && return 0
  done
  return 1
}

assert_known_package() {
  local candidate="$1"
  [[ -z "$candidate" ]] && return 0
  for package in "${all_packages[@]}"; do
    [[ "$package" == "$candidate" ]] && return 0
  done
  echo "Unknown package: $candidate" >&2
  echo "Known packages: ${all_packages[*]}" >&2
  exit 2
}

run_python_task() {
  local package="$1"
  local task="$2"
  local package_path
  case "$package" in
    sync-server-service)
      package_path="apps/sync-server/service"
      ;;
    studio-service)
      package_path="apps/studio/service"
      ;;
    python-shared)
      package_path="packages/python-shared"
      ;;
    *)
      echo "Unknown Python package: $package" >&2
      exit 2
      ;;
  esac
  uv run --package "$package" --group hooks poe -C "$package_path" "$task"
}

run_browser_task() {
  local package="$1"
  local task="$2"
  pnpm --filter "$package" "$task"
}

for_selected_python() {
  local task="$1"
  if [[ -n "$package_name" ]]; then
    is_python_package "$package_name" && run_python_task "$package_name" "$task"
    return 0
  fi
  for package in "${python_packages[@]}"; do
    run_python_task "$package" "$task"
  done
}

for_selected_browser() {
  local task="$1"
  if [[ -n "$package_name" ]]; then
    is_browser_package "$package_name" && run_browser_task "$package_name" "$task"
    return 0
  fi
  for package in "${browser_packages[@]}"; do
    run_browser_task "$package" "$task"
  done
}

run_for_selection() {
  local python_task="$1"
  local browser_task="$2"
  assert_known_package "$package_name"
  if [[ -n "$package_name" ]]; then
    if is_python_package "$package_name"; then
      run_python_task "$package_name" "$python_task"
    else
      run_browser_task "$package_name" "$browser_task"
    fi
    return 0
  fi
  for_selected_python "$python_task"
  for_selected_browser "$browser_task"
}

case "$command_name" in
  setup)
    uv sync --all-groups
    pnpm install
    ;;
  setup:lint)
    uv sync --group lint --group hooks
    pnpm install
    ;;
  setup:typecheck)
    uv sync --group typecheck --group hooks
    pnpm install
    ;;
  setup:test)
    uv sync --group test --group coverage --group recording --group hooks
    pnpm install
    ;;
  lint)
    uv sync --group lint --group hooks
    run_for_selection lint lint
    ;;
  typecheck)
    uv sync --group typecheck --group hooks
    run_for_selection typecheck typecheck
    ;;
  test)
    uv sync --group test --group hooks
    run_for_selection test test
    ;;
  coverage)
    uv sync --group test --group coverage --group hooks
    assert_known_package "$package_name"
    for_selected_python coverage
    ;;
  openapi)
    uv sync --group hooks
    assert_known_package "$package_name"
    for_selected_python openapi
    ;;
  orval)
    pnpm install
    assert_known_package "$package_name"
    for_selected_browser orval
    ;;
  generated-check)
    "$0" openapi "$package_name"
    "$0" orval "$package_name"
    git diff --exit-code -- apps packages
    ;;
  har:record)
    pnpm install
    assert_known_package "$package_name"
    for_selected_browser test:record
    ;;
  har:test)
    pnpm install
    assert_known_package "$package_name"
    for_selected_browser test
    ;;
  docs)
    npx -y @probelabs/maid docs/
    ;;
  version-check)
    uv sync --group version --group hooks
    uv run python scripts/version_check.py "${package_name:-}"
    ;;
  check)
    "$0" lint "$package_name"
    "$0" typecheck "$package_name"
    "$0" test "$package_name"
    "$0" coverage "$package_name"
    "$0" generated-check "$package_name"
    "$0" version-check "$package_name"
    "$0" docs
    ;;
  check:ci)
    "$0" lint "$package_name"
    "$0" typecheck "$package_name"
    "$0" test "$package_name"
    "$0" version-check "$package_name"
    ;;
  build)
    run_for_selection build build
    ;;
  *)
    echo "Usage: $0 <command> [package]" >&2
    exit 2
    ;;
esac
