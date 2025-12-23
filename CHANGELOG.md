# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2025-12-23

### Changed
- Modified `POST`, `PUT` and `PATCH` wrappers in the connection to allow optional query parameters (addresses PR#8)
- Removed default TTL from CNAME records (PR#6)

### Fixed
- `add_list` and `update_list` now correctly pass the `list_type` as a query parameter (addresses PR#8)

## [0.2.0] - 2025-06-03

### Added

- `get_all_domains` method in `domain_management` which returns all whitelisted and blacklisted domains.
- `version` method to base client which returns current client version. 
- `CHANGELOG.md` with a retroactive summary of releases.
- `CONTRIBUTING.md` with basic contribution guidelines.

### Changed

- Improved exception message when no password or an invalid password is supplied.

## [0.1.9] - 2025-04-17

### Added

- Retry support for failed requests using `urllib3.Retry`, including:
  - Configurable `max_retries` and `retry_delay` parameters with exponential backoff.
  - Retry conditions for HTTP 429, 500, 502, 503, and 504 status codes.
- Connection pooling options via the `disable_connection_pooling` parameter.
- `connection_timeout` parameter (default: 10 seconds) to avoid indefinite hangs during network issues.
- A logger (`logging.getLogger("pihole6api")`) for debug and error output covering:
  - Authentication attempts
  - Retry timing
  - Request errors and timeouts

### Changed

- Configured a `requests.Session()` with a custom `HTTPAdapter` to enforce retry and pooling behavior.
- Set `self.session.timeout` globally based on the `connection_timeout` setting.
- Improved error handling to extract and display more detailed messages from API responses when authentication fails repeatedly.

## [0.1.8] - 2025-03-31

### Fixed

- Bug in `metrics.get_queries` method:
  - Endpoint originally used `n` as the parameter to control the number of queries returned.
  - Correct parameter is `length`.
  - For backwards compatibility, both `n` and `length` are now accepted (the `n` parameter will be removed in a future release).

## [0.1.7] - 2025-03-18

### Added

- `get_clients()` method in `client_management`.

### Fixed

- Docstring in `batch_delete_lists()` updated to accurately reflect the correct object parameters.

## [0.1.6] - 2025-03-16

### Added

- `get_groups()` method in `group_management`.

### Fixed

- In `list_management`, removed the now-invalid optional `list_type` parameter from `update_list`.

## [0.1.5] - 2025-03-16

### Added

- `get_lists()` method in `list_management`.

## [0.1.4] - 2025-02-22

### Added

- Missing query parameters to `list_management.get_list`.
- Optional parameters to `list_management.search_list`.
- `nextID` query parameter for incremental log retrieval in:
  - `ftl_info.get_dnsmasq_logs`
  - `ftl_info.get_ftl_logs`
  - `ftl_info.get_webserver_logs`
- Additional optional flags for network info retrieval:
  - `network_info.get_devices` now supports filtering options.
  - `network_info.get_gateway` now supports a `detailed` flag.
  - `network_info.get_interfaces` now supports a `detailed` flag.
  - `network_info.get_routes` now supports a `detailed` flag.

### Fixed

- Added missing `json` import in `PiHole6Connection`.

## [0.1.3] - 2025-02-22

### Fixed

- Refactored authentication module to improve reliability in Ansible:
  - Removed code that attempted to serialize non-JSON responses into JSON (which was causing secondary exceptions).
  - Added a retry mechanism to handle transient failures in authentication requests.

## [0.1.2] - 2025-02-22

### Added

- `close_session()` method in the client to clean up after authentication (calling `client.close_session()` sends a DELETE request to `/auth` and allows subsequent requests to re-authenticate and create a new session).

## [0.1.1] - 2025-02-22

### Added

- Simplified methods for adding local A records and CNAMEs.
- Added missing and optional parameters to metrics API methods:
  - `metrics.get_history_clients` (added `n` parameter)
  - `metrics.get_history_database` (added `start` and `end`)
  - `metrics.get_history_database_clients` (added `start` and `end`)
  - `metrics.queries` (added granular filter parameters)
  - `metrics.get_stats_database_query_types` (added `start` and `end`)
  - `metrics.get_stats_database_top_clients` (added required params and filters)
  - `metrics.get_stats_database_top_domains` (added required params and filters)
  - `metrics.get_stats_database_upstreams` (added `start` and `end`)
  - `metrics.get_stats_recent_blocked` (added `count`)
  - `metrics.get_stats_top_clients` and `metrics.get_stats_top_domains` (added `block` and `count`)

## [0.1.0] - 2025-02-22

### Added
- Initial release of `pihole6api`, a Python API client for Pi-hole 6.
- Session-based authentication with automatic renewal.
- Modular structure with separate API components.
- Full support for Pi-hole's v6 API, including statistics, configuration, and management.
- Graceful handling of errors.