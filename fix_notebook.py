import json
import os

def fix_notebook(input_path, output_path=None):
    """Fix Jupyter notebook formatting issues"""
    if output_path is None:
        output_path = input_path.replace('.ipynb', '_fixed.ipynb')
    
    print(f'🔧 Fixing notebook: {input_path}')
    
    try:
        # Read the notebook
        with open(input_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Fix 1: Remove problematic metadata.widgets if it exists
        if 'metadata' in notebook and 'widgets' in notebook['metadata']:
            print('  Removing problematic widgets metadata...')
            del notebook['metadata']['widgets']
        
        # Fix 2: Clean up metadata
        if 'metadata' not in notebook:
            notebook['metadata'] = {}
        
        # Ensure required metadata fields
        if 'kernelspec' not in notebook['metadata']:
            notebook['metadata']['kernelspec'] = {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3'
            }
        
        if 'language_info' not in notebook['metadata']:
            notebook['metadata']['language_info'] = {
                'name': 'python',
                'version': '3.8.0'
            }
        
        # Fix 3: Clean up each cell
        for i, cell in enumerate(notebook['cells']):
            # Ensure cell_type exists
            if 'cell_type' not in cell:
                cell['cell_type'] = 'code'  # Default to code
            
            # Ensure source is a list
            if 'source' in cell:
                if isinstance(cell['source'], str):
                    cell['source'] = [cell['source']]
                elif not isinstance(cell['source'], list):
                    cell['source'] = [str(cell['source'])]
            else:
                cell['source'] = ['']
            
            # Clean up outputs
            if 'outputs' in cell:
                if not cell['outputs'] or cell['outputs'] == []:
                    del cell['outputs']
            
            # Fix execution_count
            if 'execution_count' in cell and cell['execution_count'] is None:
                cell['execution_count'] = 0
        
        # Fix 4: Ensure nbformat version
        if 'nbformat' not in notebook:
            notebook['nbformat'] = 4
        if 'nbformat_minor' not in notebook:
            notebook['nbformat_minor'] = 0
        
        # Write fixed notebook
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)
        
        print(f'✅ Fixed notebook saved as: {output_path}')
        print(f'📊 Notebook info:')
        print(f'   Cells: {len(notebook["cells"])}')
        print(f'   Size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB')
        
        return True
        
    except Exception as e:
        print(f'❌ Error fixing notebook: {e}')
        return False

if __name__ == "__main__":
    # Fix the notebook
    fix_notebook('notebooks/financial_sentiment_analysis.ipynb')
