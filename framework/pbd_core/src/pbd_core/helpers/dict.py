from typing import Any, Dict


class DictHelper:

    @classmethod
    def flatten(self, source: dict, parent_key='', sep='.') -> Dict:
        result = {}
        for k, v in source.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                # 即使v是空字典，也要保留它
                flattened = self.flatten(v, new_key, sep=sep)
                if not flattened:  # 如果子字典是空的
                    result[new_key] = {}
                else:
                    result.update(flattened)
            else:
                result[new_key] = v
        return result
    
    @classmethod
    def find_by_path(self, source: dict, path: str, sep='.') -> Any:
        if not path:  # 空路径返回None
            return None
            
        keys = path.split(sep)
        current = source
        
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        
        return current

    @classmethod
    def deep_clone(self,source: Dict) -> Dict:
        """深度拷贝字典并移除标记"""
        return {
            k: DictHelper.deep_clone(v) if isinstance(v, dict) else v
            for k, v in source.items()
            if k != '__public__'
        }
    
    @classmethod 
    def deep_merge(self,target: Dict, source: Dict):
        """递归合并字典"""
        for k, v in source.items():
            if isinstance(v, dict):
                node = target.setdefault(k, {})
                DictHelper.deep_merge(node, v)
            else:
                target[k] = v
