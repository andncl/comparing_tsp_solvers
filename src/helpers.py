"""Module containing helper functions"""

def sequences_are_equal(seq_1: str, seq_2):
    """
    Checks if given sequences are equal or permutations of eachother
    
    Args:
        seq_1 (str): Sequence 1
        seq_2 (str): Sequence 2
    
    Returns:
        bool: True if sequences are equal or permuattions
    """
    if list(seq_1)[0] != '0' or list(seq_2)[0] != '0':
        raise ValueError("Sequence has to start in the first city!")
    if seq_1 == seq_2:
        return True
    seq_2 = '0' + ''.join((reversed(list(seq_2)[1:])))
    if seq_1 == seq_2:
        return True
    return False