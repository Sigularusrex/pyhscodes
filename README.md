# pyhscodes

A Python package for working with Harmonized System (HS) codes from the World Customs Organization. Built on the foundation of the popular [pycountry](https://github.com/flyingcircusio/pycountry) package, pyhscodes provides a similar API for HS codes with hierarchical structure and search capabilities.

## Features

- **Complete HS Code Database**: Contains 6,940+ HS codes with full hierarchical structure
- **Regulatory Standards**: Built-in support for EUDR, EUTR, and CBAM with extensible standards framework
- **Section Support**: All 21 HS code sections with descriptions
- **Hierarchical Navigation**: Navigate from chapters (2-digit) to headings (4-digit) to subheadings (6-digit)
- **Fuzzy Search**: Find codes by description text
- **Fast Lookups**: Optimized indexing for quick code retrieval
- **Pythonic API**: Clean, intuitive interface similar to pycountry

## Installation

```bash
pip install pyhscodes
```

## Quick Start

```python
import pyhscodes

# Basic statistics
print(f"Total HS codes: {len(pyhscodes.hscodes)}")
print(f"Total sections: {len(pyhscodes.sections)}")

# Get a specific code
animals = pyhscodes.hscodes.get(hscode="01")
print(f"{animals.hscode}: {animals.description}")
print(f"Section: {animals.section_name}")  # "live animals; animal products"

# Get children of a code
children = pyhscodes.hscodes.get_children("01")
for child in children:
    print(f"  {child.hscode}: {child.description}")

# Get full hierarchy
hierarchy = pyhscodes.hscodes.get_hierarchy("010121")
for code in hierarchy:
    print(f"{code.hscode}: {code.description} (Level {code.level})")

# Fuzzy search
results = pyhscodes.hscodes.search_fuzzy("dairy")
for result in results[:3]:
    print(f"{result.hscode}: {result.description}")

# Check regulatory standards
timber = pyhscodes.hscodes.get(hscode="4401")
print(f"Standards: {timber.standards}")  # e.g., ["EUDR", "EUTR"]
print(f"EUDR applicable: {timber.EUDR}")
```

## API Reference

### HS Codes

#### `pyhscodes.hscodes`

The main database of HS codes.

**Properties:**
- `hscode`: The HS code (e.g., "010121")
- `description`: Description of the code
- `section`: Section identifier (e.g., "I", "II")
- `section_info`: Full Section object with all section data
- `section_name`: Full name of the section
- `section_display_name`: Short display name for the section
- `parent`: Parent code in the hierarchy
- `level`: Code level ("2", "4", or "6")
- `standards`: List of applicable regulatory standards (e.g., `["EUDR", "CBAM"]`)
- `EUDR`: Boolean indicating EU Deforestation Regulation applicability
- `EUTR`: Boolean indicating EU Timber Regulation applicability
- `CBAM`: Boolean indicating Carbon Border Adjustment Mechanism applicability
- `is_chapter`: True if this is a 2-digit chapter
- `is_heading`: True if this is a 4-digit heading  
- `is_subheading`: True if this is a 6-digit subheading

**Methods:**
- `get(hscode="01")`: Get a specific code
- `lookup("01")`: Lookup by code or description
- `search_fuzzy("horses")`: Fuzzy search by description
- `get_by_level("2")`: Get all codes at a specific level
- `get_children("01")`: Get child codes
- `get_hierarchy("010121")`: Get full hierarchy path

### Sections

#### `pyhscodes.sections`

Database of HS code sections.

**Properties:**
- `section`: Section identifier (e.g., "I", "II")
- `name`: Section name/description

**Methods:**
- `get(section="I")`: Get a specific section

## Data Structure

HS codes follow a hierarchical structure:

- **Sections**: 21 major groupings (I through XXI)
- **Chapters**: 97 two-digit codes (01, 02, ..., 97)
- **Headings**: 1,229+ four-digit codes (0101, 0102, ...)
- **Subheadings**: 5,613+ six-digit codes (010121, 010122, ...)

Example hierarchy:
```
Section I: Live animals; animal products
├── 01: Animals; live
    ├── 0101: Horses, asses, mules and hinnies; live
        ├── 010121: Horses; live, pure-bred breeding animals
        └── 010129: Horses; live, other than pure-bred breeding animals
```

## Examples

See `example.py` for a comprehensive demonstration of the package features.

## Development

### Setting up for development

```bash
git clone https://github.com/yourusername/pyhscodes.git
cd pyhscodes
pip install -e .
```

### Running tests

```bash
pytest src/pyhscodes/tests/
```

### Data Updates

To update the HS codes database:

1. Place your CSV files in the project root:
   - `harmonized-system-with-standards.csv` (columns: section, hscode, description, parent, level, EUDR, EUTR, CBAM)
   - `sections.csv` (columns: section, name)

2. Run the conversion script:
   ```bash
   python convert_csv_to_json.py
   ```

## Changelog

### 2.0.0 (Breaking Change)

- **Added section lookup properties**: HS codes now include `section_info`, `section_name`, and `section_display_name` for easy access to section data
- **Added `standards` array**: Each HS code now includes a `standards` list containing the names of applicable regulatory standards (e.g., `["EUDR", "CBAM"]`)
- **Added regulatory standard flags**: Each HS code now includes boolean fields for EU regulatory standards:
  - `EUDR`: EU Deforestation Regulation applicability
  - `EUTR`: EU Timber Regulation applicability  
  - `CBAM`: Carbon Border Adjustment Mechanism applicability
- **Extensible standards**: New standards can be added by including uppercase columns in the CSV source
- **Data source changed**: Now uses `harmonized-system-with-standards.csv` instead of `harmonized-system.csv`
- **Breaking**: HS code entries now have additional fields that may affect serialization or data processing

### 1.0.x

- Initial release with core HS code database
- Hierarchical navigation and fuzzy search
- Section support

## License

This project is licensed under the LGPL-2.1 License - see the LICENSE file for details.

## Acknowledgments

- Built on the foundation of [pycountry](https://github.com/flyingcircusio/pycountry)
- HS codes from the World Customs Organization
- Inspired by the need for a Python package similar to pycountry but for trade classification codes 