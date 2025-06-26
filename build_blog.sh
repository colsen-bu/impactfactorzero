#!/bin/bash
# Development script for building the blog with virtual environment

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🔧 Building Impact Factor Zero blog...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo -e "${YELLOW}Run ./setup_env.sh first to create the virtual environment.${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if required packages are installed
python -c "import frontmatter, markdown" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Required packages not found!${NC}"
    echo -e "${YELLOW}Installing packages from requirements.txt...${NC}"
    pip install -r requirements.txt
fi

# Run the blog builder
echo -e "${YELLOW}🚀 Running blog builder...${NC}"
python .github/scripts/build_blog.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Blog build completed successfully!${NC}"
else
    echo -e "${RED}❌ Blog build failed!${NC}"
    exit 1
fi

# Deactivate virtual environment
deactivate
echo -e "${GREEN}🎉 Done! Virtual environment deactivated.${NC}"
