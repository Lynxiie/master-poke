from typing import Sequence


def sort_by_previous_value[T](array: Sequence[T]) -> Sequence[T]:
    """
    Tri une liste selon une valeur "after"
    :param array: une liste d'événement
    :return: le liste trié
    """
    if not hasattr(array[0], 'after'):
        return array

    output = []
    rank = 0

    for index in range(len(array)):
        for item in array:
            if item.after == rank:
                output.append(item)
                rank = item.id

    return output


def change_order[T](array: Sequence[T], element_to_move: T, new_rank: int):
    """
    Change l'ordre d'événements
    :param array: une liste d'événement avec une propriété "after"
    :param element_to_move: l'élément à bouger
    :param new_rank: le rang du nouvel élément
    """
    if not hasattr(array[0], 'after') or element_to_move.after == new_rank or element_to_move.id == new_rank:
        return

    old_rank = element_to_move.after
    after_before_move = next((item for item in array if item.after == element_to_move.id), None)
    after_after_move = next((item for item in array if item.after == new_rank), None)

    if after_before_move:
        after_before_move.after = old_rank
    if after_after_move:
        after_after_move.after = element_to_move.id
    element_to_move.after = new_rank
