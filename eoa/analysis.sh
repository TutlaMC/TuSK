#!/bin/bash

echo "=== Code Analysis Report ==="
echo

# Initialize counters
total_lines=0
total_classes=0
total_functions=0
total_imports=0
total_comments=0

# Initialize file type counters
declare -A file_types
declare -A file_type_lines

echo "File Analysis:"
echo "----------------------------------------"

# Process each file in the current directory, excluding .git and hidden folders
while IFS= read -r file; do
    # Get file extension
    extension="${file##*.}"
    if [ -z "$extension" ]; then
        extension="no_extension"
    fi
    
    # Update file type counters
    file_types[$extension]=$((file_types[$extension] + 1))
    
    echo -n "$file: "
    
    # Count non-empty lines
    lines=$(grep -v '^\s*$' "$file" | wc -l)
    total_lines=$((total_lines + lines))
    file_type_lines[$extension]=$((file_type_lines[$extension] + lines))
    
    # Only count Python-specific metrics for .py files
    if [ "$extension" = "py" ]; then

        classes=$(grep -c "^class " "$file")
        total_classes=$((total_classes + classes))
        
        functions=$(grep -c "^    def " "$file")
        total_functions=$((total_functions + functions))
        
        imports=$(grep -c "^import\|^from " "$file")
        total_imports=$((total_imports + imports))
        
        comments=$(grep -c "^#" "$file")
        total_comments=$((total_comments + comments))
        
        echo "$lines lines, $classes classes, $functions functions, $imports imports, $comments comments"
    else
        echo "$lines lines"
    fi
done < <(find . -type d -name .git -prune -o -type f -print)

echo "----------------------------------------"
echo "Summary by File Type:"
echo "----------------------------------------"
for ext in "${!file_types[@]}"; do
    echo "$ext files: ${file_types[$ext]} (${file_type_lines[$ext]} lines)"
done

echo "----------------------------------------"
echo "Python Code Summary:"
echo "Total lines of code: $total_lines"
echo "Total classes: $total_classes"
echo "Total functions: $total_functions"
echo "Total imports: $total_imports"
echo "Total comments: $total_comments"
echo
echo "Code Structure:"

# Calculate averages only if there are Python files
python_files=$(find . -type d -name .git -prune -o -type f -name "*.py" -print | wc -l)
if [ "$python_files" -gt 0 ]; then
    if [ "$total_classes" -gt 0 ]; then
        avg_functions=$(echo "scale=2; $total_functions/$total_classes" | bc 2>/dev/null || echo "N/A")
        echo "- Average functions per class: $avg_functions"
    else
        echo "- Average functions per class: N/A (no classes found)"
    fi
    
    avg_lines=$(echo "scale=2; $total_lines/$python_files" | bc 2>/dev/null || echo "N/A")
    echo "- Average lines per file: $avg_lines"
    
    if [ "$total_lines" -gt 0 ]; then
        comment_ratio=$(echo "scale=2; $total_comments/$total_lines*100" | bc 2>/dev/null || echo "N/A")
        echo "- Comment ratio: $comment_ratio%"
    else
        echo "- Comment ratio: N/A (no lines of code)"
    fi
else
    echo "- No Python files found in the current directory"
fi 