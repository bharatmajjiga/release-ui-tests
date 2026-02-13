# Openshift Pipelines UI Automation Framework (opuiafw)

## Installation
- Clone this repository (if using virtualenvwrapper, be sure to clone from your virtual environment) using your local
user (do not clone using root):
```
git clone git@github.com:openshift-pipelines/release-ui-tests.git
```

### Dependencies Installation for Linux

#### Debian/Ubuntu

- Install required dependencies
```
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    llvm libncursesw5-dev xz-utils tk-dev \
    libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev git
```
- Install pyenv and pyenv-virtualenv
```
curl https://pyenv.run | bash
```

- Add pyenv setup to your shell configuration file (e.g., ~/.bashrc or ~/.zshrc)
```
echo -e '\n# pyenv setup' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'eval "$(pyenv init --path)"\neval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```
- Reload shell configuration
```
source ~/.bashrc
```

#### Fedora

- Install required dependencies
```
sudo dnf update -y
sudo dnf install @development-tools @c-development
sudo dnf install zlib-devel bzip2-devel openssl-devel ncurses-devel \
sqlite-devel readline-devel tk-devel gdbm-devel libpcap-devel \
xz-devel libffi-devel libuuid-devel
```
- Install pyenv and pyenv-virtualenv
```
curl https://pyenv.run | bash
```

- Add pyenv setup to your shell configuration file (e.g., ~/.bashrc or ~/.zshrc)
```
echo -e '\n# pyenv setup' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'eval "$(pyenv init --path)"\neval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
```
- Reload shell configuration
```
source ~/.bashrc
```

#### Mac OS
- Install pyenv and pyenv-virtualenv
```
brew install pyenv pyenv-virtualenv
```
- Add pyenv setup to your shell configuration file (e.g., ~/.bashrc or ~/.zshrc)
```
echo -e '\neval "$(pyenv init --path)"\neval "$(pyenv virtualenv-init -)"' >> ~/.zshrc
```
- Reload shell configuration
```
source ~/.zshrc
```
### Enter the project directory and install it using pip:

- Install Python version 3.13.6
```
pyenv install 3.13.6
```
- Navigate to the project directory
```
cd release-ui-tests
```
- Create virtual environment
```
pyenv virtualenv 3.13.6 .venv
```
- Set the local Python version to the newly created virtualenv
```
pyenv local .venv
```
- Install project dependencies
```
pip install -r requirements.txt
```

- Verify that the linter is functional:
```
pre-commit install
```
- To execute playwright based test, run the following setup:
```
### Linux/Mac OS
playwright install --with-deps

### Fedora
playwright install
```

## Executing tests

### Quick run (command line)

Set required environment variables, then run pytest (e.g. with tags):

```bash
export CONSOLE_URL="https://console-openshift-console.apps.example.com"
export CONSOLE_USERNAME="kubeadmin"
export CONSOLE_PASSWORD="<your-password>"
# Optional: export CONSOLE_AUTH_TYPE="htpasswd"   # default is kube:admin
pytest -m "smoke and e2e"
```

### Execution using pytest

- Make sure to have an env deployed by one of the following options:
  - Deploy a test env from the pipeline (TBD: link to pipeline).
- **IDE**: Open run configuration for your test and add the same env variables to the execution.
- To run by marks: `pytest -m "mark1 and mark2"` (e.g. `pytest -m "smoke and e2e"`).
- To run in parallel (one feature file per worker, session per feature): `pytest -m smoke -n auto --dist loadgroup`.

### CI

- In CI, set `CONSOLE_URL`, `CONSOLE_USERNAME`, and `CONSOLE_PASSWORD` from your pipeline secrets or config; then run `pytest` (optionally `-m "smoke and e2e"`). Use a headless browser (Playwright default when no display is available). One browser session per feature file; see **Fixtures** and **Browser session and login** in the Framework reference.


---

## Framework reference (for developers and AI)

This section describes the framework structure, conventions, and behavior so that anyone (including AI assistants) can understand, extend, or modify the automation correctly. **For extension and design details, jump to the subsections below.**

### Scope

- **In scope**: End-to-end UI automation for the OpenShift Pipelines console (login, navigation, visibility of Pipelines / Overview / Tasks / Triggers and their tabs). Focus is smoke and e2e flows.
- **Out of scope** (unless added later): Standalone API tests, performance tests, and accessibility (a11y) automation. Other OpenShift console areas are out of scope unless covered by new features.

### Python support

- **Supported version**: Python 3.13.x (see Installation for 3.13.6 setup). Compatibility with 3.11/3.12 is not formally documented; prefer the version used in CI.

### Tech stack and dependencies

| Layer        | Technology        | Purpose |
|-------------|-------------------|--------|
| Test runner | pytest 8.x        | Discovery, fixtures, reporting |
| BDD         | pytest-bdd 8.x    | Gherkin features and step definitions |
| Browser     | Playwright 1.50   | Browser automation (sync API) |
| Integration | pytest-playwright | Pytest fixtures for browser/page/context |
| Optional    | pytest-reportportal | Reporting (if configured) |

Code style and linting: **Ruff** (via pre-commit), **Flake8** (`.flake8`: max-line-length 120, complexity 10, E203 ignored).

---

### Directory structure

```
release-ui-tests/
├── framework/                    # Reusable framework code (no test logic)
│   ├── config/
│   │   ├── config.py             # Config singleton (env-based)
│   │   ├── singleton.py         # Singleton metaclass
│   │   └── pytest_args_options_fixture.py  # Pytest hooks & --ignore-ssl-errors
│   ├── fixtures/
│   │   └── ui_fixtures.py       # config, browser_context_args, page fixtures
│   └── ui_components/
│       ├── base_page.py         # Base class for all page objects
│       ├── locators.py          # Centralized locators (by page/component)
│       ├── commons/             # Shared UI (login, left nav)
│       │   ├── login_page.py
│       │   └── left_navigation_bar.py
│       ├── overview_page.py
│       ├── pipelines_overview_page.py
│       ├── pipelines_page.py
│       ├── tasks_page.py
│       └── triggers_page.py
├── tests/
│   ├── conftest.py              # Imports framework fixtures; registers step plugins
│   ├── features/                # Gherkin .feature files
│   │   ├── pipelines_smoke.feature
│   │   └── pipelines_regression.feature
│   └── steps/                   # Step definition modules
│       ├── test_common_steps.py # Shared steps (login, nav, pipelines/tasks/triggers)
│       └── test_pipeline_steps.py # scenarios("pipelines_smoke.feature", "pipelines_regression.feature") + extra steps
├── pytest.ini                   # markers (smoke, e2e), bdd_features_base_dir
├── requirements.txt
├── .flake8
└── .pre-commit-config.yaml
```

- **framework/** holds configuration, fixtures, and page objects; it does not depend on `tests/`.
- **tests/** holds feature files, step definitions, and `conftest`; it imports from `framework/`.

---

### Configuration and environment

- **Config** is a **singleton** (`framework.config.config.Config`) and must only be used **inside** class/function bodies (e.g. in `__init__` or step functions). Do not assign `Config` values to module-level constants—that can capture an uninitialized or wrong config.
- Required environment variables (validated at session start):
  - `CONSOLE_URL` — OpenShift console base URL
  - `CONSOLE_USERNAME` — Login username (e.g. kubeadmin)
  - `CONSOLE_PASSWORD` — Login password
- Optional:
  - `APP_TIMEOUT` — Timeout in milliseconds (default `90000`).
  - `CONSOLE_AUTH_TYPE` — Login auth type (default `kube:admin`; e.g. `htpasswd`). Exposed as `Config.auth_type`; used when the fixture logs in once per feature file.
- Pytest option: `--ignore-ssl-errors` (default True). Set to false to enforce SSL.

Config is created at session start via `pytest_sessionstart` in `pytest_args_options_fixture.py`.

---

### Fixtures (from `framework.fixtures.ui_fixtures`)

- **Scope**: `config` and `browser_context_args` are **session**-scoped. **page** is **function**-scoped but **one browser session per feature file**: all scenarios from the same `.feature` file share the same browser context and page; scenarios from another `.feature` file get a different session. You can bind multiple features in a single step module (e.g. `scenarios("a.feature")` and `scenarios("b.feature")`) without creating a separate step file per feature. See **Browser session and login** below for how this and login-once work.
- **config** (session): Returns the `Config` singleton.
- **browser_context_args** (session): Sets Playwright context options (e.g. viewport 1920x1080, `ignore_https_errors` from `--ignore-ssl-errors`). Navigation timeout is set on the context when the **page** session is created.
- **feature_browser_sessions** (session): Internal cache keyed by feature file path (from pytest-bdd `__scenario__.feature.filename`). Each key maps to a `(BrowserContext, Page)`. Created when the **page** fixture is first requested for that feature; all contexts are closed at session teardown.
- **page** (function): Main fixture used by steps. It returns a **dict** of page objects (rather than a raw Playwright page) so a single fixture can expose multiple screens (login, nav, pipelines, tasks, triggers, etc.) and steps access them by key, e.g. `page["login"]`, `page["nav"]`. Session is keyed by feature file path via `get_feature_file_path(request)`; non–pytest-bdd tests fall back to the test module (nodeid prefix). When a feature file’s session is created for the first time, **login runs once** via `_login_once_for_feature(raw_page, config)`—navigate to console, choose auth from `config.auth_type`, submit credentials, verify Overview. No Background step is required. The fixture:
  - Sets `page.set_default_timeout(config.timeout_ms)` and `context.set_default_navigation_timeout(config.timeout_ms)` when creating a new session.
  - Provides the dict with keys:
    - `raw_page` — Playwright `Page`
    - `login` — `LoginPage`
    - `nav` — `LeftNavigationBar`
    - `overview` — `OverViewPage`
    - `pipelines_overview` — `PipelinesOverViewPage`
    - `pipelines` — `PipelinesPage`
    - `tasks` — `TasksPage`
    - `triggers` — `TriggersPage`

Step definitions receive this dict as the **page** parameter and use it like `page["login"]`, `page["nav"]`, etc.

### Browser session and login

- **One session per feature file**: The **page** fixture uses `get_feature_file_path(request)` to get the current pytest-bdd feature file path (`__scenario__.feature.filename`). The session-scoped cache `feature_browser_sessions` stores one `(context, page)` per feature path. So all scenarios in `pipelines_smoke.feature` share one browser session, and all in `pipelines_regression.feature` share another—even when both are bound in the same step module with `scenarios("pipelines_smoke.feature")` and `scenarios("pipelines_regression.feature")`. No need for a separate step file per feature.
- **Login once per feature file**: When the **page** fixture creates a new session for a feature path, it calls `_login_once_for_feature(raw_page, config)` immediately after creating the page. That helper navigates to the console URL, verifies the login page, chooses the auth type from `config.auth_type` (e.g. `kube:admin`), submits credentials, and verifies the Overview page. Subsequent scenarios in that feature reuse the same session and are already logged in; no Background is required.
- **Optional Background and idempotent login step**: Feature files do not need a Background. If you add a Background with the step **Given the user is logged in to the OpenShift console with {auth_type}**, it will not cause re-login on later scenarios. That step is **idempotent**: it uses `_already_logged_in(page)`, which returns True unless the current URL is `about:blank` or contains `oauth` (login page). So when the first scenario runs, the fixture has already logged in; the step sees a console URL and does nothing. When later scenarios run (e.g. on Pipelines or Tasks), the step again sees a non-login URL and does nothing. Login is performed only when the session is actually on the login page or blank.

### Test data and credentials

- Credentials and test data come from **environment variables** (and in CI, from pipeline secrets). Do not commit credentials; the repo must stay free of secrets.
- Supported login types in steps: e.g. `kube:admin`, `htpasswd`. Test env is expected to be pre-provisioned (who provisions it is pipeline/team-specific; see CI/TBD links).

### Parallelism

- **Implemented** with **pytest-xdist**. Each feature file and its scenarios are assigned the same **xdist_group** (via `pytest_collection_modifyitems` in `tests/conftest.py`, using the feature file basename). Use **`--dist loadgroup`** so all scenarios from the same feature file run on the same worker; session-per-feature is preserved per worker.
- **Run in parallel**: `pytest -n auto --dist loadgroup` (or `-n 2` for two workers). Example: `pytest -m smoke -n auto --dist loadgroup`. Each worker runs one or more feature files; within a worker, all scenarios of a given feature share one browser session (login once per feature, same as serial run).
- **How it works**: Collection adds `@pytest.mark.xdist_group("feature_name.feature")` to each test from that feature. With `--dist loadgroup`, xdist keeps the same group on the same worker. **Config** and **feature_browser_sessions** are per process, so each worker has its own sessions. No shared memory between workers (multiprocessing).
- **Known limitations**: The `_tour_skipped` flag in `overview_page.py` is per process; with xdist each worker is a separate process, so no cross-worker conflict. Thread-safety would only matter if running multiple threads per worker (not the default).

---

### Page object pattern

- **Base class**: `framework.ui_components.base_page.BasePage`. All page objects extend it. Constructor: `(self, page: Page, config: Config)`. It provides:
  - `click_element(locator, timeout=None)`
  - `fill_input(locator, value, timeout=None)`
  - `is_visible(locator, timeout=None)` — returns False on timeout
  - `wait_for_url_to_endwith(page_suffix, timeout=None)`
  - `wait_for_url_to_contain(page_substring, timeout=None)`
  - `_verify_page(expected_url_suffix, header_locator, page_name)` — URL + header check
  - `_verify_data_load(locator, tab_name, no_data_locator=None)` — wait for data or “no data” state
- **Locators**: All selectors live in `framework.ui_components.locators`. One class per page/component (e.g. `LoginPageLocators`, `LeftNavigationBarLocators`). Playwright locator strings (CSS, `:has-text()`, etc.).
- **Page classes**: Each page has a class in `framework.ui_components` (or `commons/`). They hold `self.page`, `self.config`, `self.locators` and expose methods that return `bool` (True on success; raise or return False on failure). Use `_verify_page` and `_verify_data_load` for consistent page/tab verification.

---

### Step definitions and BDD flow

- **Gherkin** files live under `tests/features/`. `pytest.ini` sets `bdd_features_base_dir = tests/features/`.
- **Step modules**:
  - Shared steps are in `tests/steps/test_common_steps.py`, which is registered in `tests/conftest.py` via `pytest_plugins = ["tests.steps.test_common_steps"]`, so their steps are available to all features.
  - A feature is bound by calling `scenarios("feature_name.feature")` in a step module (e.g. `test_pipeline_steps.py` binds both `pipelines_smoke.feature` and `pipelines_regression.feature`). That module can also define additional steps used only by those features.
- **Login step**: **Given the user is logged in to the OpenShift console with {auth_type}** is a combined step (navigate to login page, choose auth, submit credentials, verify Overview). It is **idempotent**: it skips work when `_already_logged_in(page)` is True (current URL is not `about:blank` and does not contain `oauth`). Use it in Background only if you want it documented in Gherkin; the **page** fixture already logs in once per feature file, so this step will no-op when the session is already in the console.
- **Step signature**: Steps that need the app “page” receive the **page** fixture (the dict of page objects), e.g. `def user_on_login_page(page: Dict[str, Any]) -> None`. They call `page["login"]`, `page["nav"]`, etc., and use `assert` for verification.
- **Parameterized steps**: Use `parsers.parse("... {param_name} ...")` and add the same parameter to the function, e.g. `@when(parsers.parse("user chooses to login with {auth_type}"))` with `auth_type: str`.
- **Tags**: Features/scenarios use tags like `@smoke` and `@e2e`; run with e.g. `pytest -m "smoke and e2e"`.

---

### Feature file conventions

- One feature per file; scenarios can be normal or **Scenario Outline** with **Examples**.
- **No Background required**: Login runs once per feature file inside the **page** fixture when that feature’s session is first created. Scenarios can start directly with navigation/visibility steps (e.g. “Then Validate Pipelines button is visible in the left navigation bar”).
- **Optional Background**: You may add a Background with **Given the user is logged in to the OpenShift console with kube:admin** for readability or consistency. That step is idempotent and will not re-login on later scenarios (it skips when the current URL is already in the console).
- First step of each scenario must start with **Given**, **When**, or **Then** (not **And**).
- Step text in the feature must match the decorator string exactly (or via parsers) for the step to be found.

---

### Adding new tests or pages

1. **New page**:
   - Add a locator class in `locators.py`.
   - Add a page class in `framework/ui_components/` extending `BasePage`, using the new locators and `_verify_page` / `_verify_data_load` where appropriate.
   - In `framework/fixtures/ui_fixtures.py`, instantiate the new page in the **page** fixture dict and document the key in the docstring.
2. **New steps**:
   - Either add to `test_common_steps.py` (if shared) or to a feature-specific step module. Use `@given`, `@when`, `@then` from `pytest_bdd` and the **page** fixture.
3. **New feature file**:
   - Add `feature_name.feature` under `tests/features/`.
   - In a step module (new or existing), call `scenarios("feature_name.feature")` so pytest-bdd collects the scenarios. Ensure all steps used are defined in that module or in a plugin-loaded module (e.g. `test_common_steps`).

---

### Code style and quality

- **.flake8**: max-line-length 120, E203 ignored, max-complexity 10; exclude `.git`, `__pycache__`, `.venv`, etc.
- **Pre-commit**: Ruff (lint + format, line-length 120, selected rules including ANN, I, E, F, C90) and pre-commit-hooks (no-commit-to-branch for main/master, trailing whitespace, YAML/JSON checks, etc.). Run `pre-commit install` after clone.
- Prefer docstrings for public methods and type hints for parameters and return values where established in the codebase.

### Reporting and artifacts

- Test results are reported through **pytest** (console and any configured plugins). **pytest-reportportal** is listed as an optional dependency; when configured, results can be sent to ReportPortal. Screenshots/traces on failure depend on Playwright and pytest-playwright configuration (e.g. built-in trace on failure if enabled).

### Known limitations

- **Shared state**: `_tour_skipped` in `framework.ui_components.overview_page` is per-process. With pytest-xdist (multiprocessing), each worker has its own copy, so parallel execution is safe. Thread-safety would only be needed if using multiple threads within one worker.

---

### Summary for AI agents

- **Config**: Singleton; env vars `CONSOLE_URL`, `CONSOLE_USERNAME`, `CONSOLE_PASSWORD`; optional `APP_TIMEOUT`, `CONSOLE_AUTH_TYPE` (default `kube:admin`). Exposed as `config.auth_type`. Use only inside functions/classes.
- **Browser session**: One session per feature file. The **page** fixture is keyed by pytest-bdd feature file path (`get_feature_file_path(request)` → `__scenario__.feature.filename`). You can bind multiple features in one step module with `scenarios("a.feature")` and `scenarios("b.feature")`; each feature still gets its own browser session.
- **Login**: Runs **once per feature file** when that feature’s session is first created, inside the **page** fixture via `_login_once_for_feature(raw_page, config)`. No Background is required. Optional step **Given the user is logged in to the OpenShift console with {auth_type}** is idempotent (`_already_logged_in(page)` skips when URL is not `about:blank` and does not contain `oauth`), so adding it in Background does not cause re-login on later scenarios.
- **page fixture**: Dict of page objects (`raw_page`, `login`, `nav`, `overview`, `pipelines_overview`, `pipelines`, `tasks`, `triggers`). Steps use `page["key"]` to drive the UI.
- **Pages**: Subclasses of `BasePage`; locators in `locators.py`; methods return bool or raise.
- **Steps**: In `tests/steps/`; shared steps in `test_common_steps` (plugin); bind a feature with `scenarios("file.feature")` in a step module.
- **Run**: Set env vars (`CONSOLE_URL`, `CONSOLE_USERNAME`, `CONSOLE_PASSWORD`; optionally `CONSOLE_AUTH_TYPE`), then `pytest` (optionally `-m "smoke and e2e"`). **Parallel**: `pytest -n auto --dist loadgroup` so each feature file runs on one worker with one session per feature. Playwright: `playwright install` (or `--with-deps` on Linux/macOS).


### Contribution guidelines ###

TBD (see repo maintainers).

### Who do I talk to? ###

* QE team members
