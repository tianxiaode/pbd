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
        
        # 处理前n-1个keys，必须都是字典
        for key in keys[:-1]:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        
        # 处理最后一个key
        if isinstance(current, dict) and keys[-1] in current:
            return current[keys[-1]]
        return None


