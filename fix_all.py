import json
import os

def fix_notebook_completely(input_path):
    """Completely fix all notebook issues"""
    print(f'🔧 Comprehensive fix for: {input_path}')
    
    try:
        # Read the notebook
        with open(input_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Fix 1: Ensure nbformat version
        notebook['nbformat'] = 4
        notebook['nbformat_minor'] = 0
        
        # Fix 2: Ensure metadata structure
        if 'metadata' not in notebook:
            notebook['metadata'] = {}
        
        # Remove problematic widgets
        if 'widgets' in notebook['metadata']:
            del notebook['metadata']['widgets']
        
        # Add required metadata
        notebook['metadata']['kernelspec'] = {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        }
        
        notebook['metadata']['language_info'] = {
            'name': 'python',
            'version': '3.8.0'
        }
        
        # Fix 3: Fix each cell completely
        for i, cell in enumerate(notebook['cells']):
            # Ensure cell_type
            if 'cell_type' not in cell:
                cell['cell_type'] = 'code'
            
            # Ensure source is a list
            if 'source' in cell:
                if isinstance(cell['source'], str):
                    cell['source'] = [cell['source']]
            else:
                cell['source'] = ['']
            
            # Fix for code cells
            if cell['cell_type'] == 'code':
                # Ensure execution_count
                if 'execution_count' not in cell:
                    cell['execution_count'] = i + 1
                elif cell['execution_count'] is None:
                    cell['execution_count'] = i + 1
                
                # Ensure outputs exists (required property)
                if 'outputs' not in cell:
                    cell['outputs'] = []
                elif not isinstance(cell['outputs'], list):
                    cell['outputs'] = []
            
            # Fix for markdown cells
            elif cell['cell_type'] == 'markdown':
                # Remove code-specific fields
                cell.pop('execution_count', None)
                cell.pop('outputs', None)
        
        # Create output path
        output_path = input_path.replace('.ipynb', '_github_ready.ipynb')
        
        # Write fixed notebook
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)
        
        print(f'✅ Fixed notebook saved as: {output_path}')
        print(f'📊 Stats:')
        print(f'   Cells: {len(notebook["cells"])}')
        print(f'   Size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB')
        
        # Verify the fix
        verify_notebook(output_path)
        
        return output_path
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return None

def verify_notebook(notebook_path):
    """Verify notebook is valid"""
    print(f'🔍 Verifying: {notebook_path}')
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Check required properties
        required_top = ['cells', 'metadata', 'nbformat', 'nbformat_minor']
        for prop in required_top:
            if prop not in notebook:
                print(f'   ❌ Missing top-level: {prop}')
                return False
        
        # Check each cell
        valid_cells = 0
        for i, cell in enumerate(notebook['cells']):
            if 'cell_type' not in cell:
                print(f'   ❌ Cell {i}: Missing cell_type')
                continue
            
            if 'source' not in cell:
                print(f'   ❌ Cell {i}: Missing source')
                continue
            
            if cell['cell_type'] == 'code':
                if 'outputs' not in cell:
                    print(f'   ❌ Code cell {i}: Missing outputs')
                    continue
            
            valid_cells += 1
        
        print(f'   ✅ Valid cells: {valid_cells}/{len(notebook["cells"])}')
        return valid_cells == len(notebook['cells'])
        
    except Exception as e:
        print(f'   ❌ Verification failed: {e}')
        return False

# Run the fix
if __name__ == "__main__":
    input_path = "notebooks/financial_sentiment_analysis.ipynb"
    fixed_path = fix_notebook_completely(input_path)
    
    if fixed_path:
        print(f'\n🎉 Fix completed successfully!')
        print(f'   Replace: {input_path} with {fixed_path}')
