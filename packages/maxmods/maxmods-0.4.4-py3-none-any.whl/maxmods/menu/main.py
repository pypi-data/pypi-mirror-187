import os
class CallerError(BaseException): ...
class MenuException(BaseException): ...
class Base:
    """Base class for creating and managing menus.

    This class provides the basic functionality for creating and managing menus. It includes methods for adding, updating, and removing items from the menu, as well as for running the menu and handling exceptions.

    The docstrings for this class were written by OpenAI.
    
    Parameters
    ----------
    Title : str, optional
        The title of the menu.
    Class : object, optional
        The class associated with the menu.
    Item : list, optional
        A list of items in the menu, each represented as a list with the following elements:
            - The caller for the item (an integer that specifies the position of the item in the menu).
            - The text of the item.
            - The function to call when the item is selected, along with any arguments and keyword arguments.
    inText : str, optional
        The text to display when requesting user input.

    Attributes
    ----------
    Title : str
        The title of the menu.
    Class : object
        The class associated with the menu.
    Item : list
        A list of items in the menu, each represented as a list with the following elements:
            - The caller for the item (an integer that specifies the position of the item in the menu).
            - The text of the item.
            - The function to call when the item is selected, along with any arguments and keyword arguments.
    inText : str
        The text to display when requesting user input.

    """
    def __init__(self, Title = None, Class = None, Item = None, inText = 'Selection: '):
        '''
        Underlying Base class of all Menu objects.
        '''
        self.Title = Title
        self.Class = Class
        self.inText = inText
        if Item is None:
            self.Item = [[0, 'Exit', (None, None), {}]]
        else: self.Item = Item
    def add_item(self, Caller, Text, *args, **kwargs):
        """Add an item to the menu.

        This method adds an item to the menu at the specified position. If the position is already occupied, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position at which to add the item in the menu.
        Text : str
            The text of the item.
        args : tuple
            The arguments to pass to the function when the item is selected.
        kwargs : dict
            The keyword arguments to pass to the function when the item is selected.

        Raises
        ------
        CallerError
            If the specified position is already occupied.

        """
        for item in self.Item:
            if item[0] == Caller:
                raise CallerError('Defined Caller is already in use.')
        row = [Caller, Text, args, kwargs]
        self.Item.append(row)
    def update_item(self, Caller, Text, *args, **kwargs):
        """Update an item in the menu.

        This method updates an item in the menu at the specified position. If the specified position does not exist, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position of the item to update in the menu.
        Text : str
            The new text of the item.
        args : tuple
            The new arguments to pass to the function when the item is selected.
        kwargs : dict
            The new keyword arguments to pass to the function when the item is selected.

        Raises
        ------
        CallerError
            If the specified position does not exist.

        """
        self.remove_item(Caller)
        row = [Caller, Text, args, kwargs]
        self.Item.append(row)
    def remove_item(self, Caller):
        """Remove an item from the menu.

        This method removes an item from the menu at the specified position. If the specified position does not exist, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position of the item to remove from the menu.

        Raises
        ------
        CallerError
            If the specified position does not exist.

        """
        for item in self.Item:
            if item[0] == Caller:
                self.Item.remove(item)
                return
        raise CallerError('Defined Caller does not exist')
    def _Refresh(self):
        os.system('cls')
    def run(self, Caller = 0):
        """Run the menu.

        This method creates the menu and displays it to the user. It handles menu exceptions and prints them to the screen.

        Parameters
        ----------
        Caller : int, optional
            The type of menu to create, by default 0.
            0 : basic menu, accepts user input and calls the associated function when an item is selected
            1 : info menu, displays information without accepting user input
            2 : settings menu, accepts user input and updates an attribute of the associated class when an item is selected

        """
        self._Refresh()
        text = f'{self.Title}\n'
        self.Item.sort(key=lambda x:x[0])
        for i, item in enumerate(self.Item):
            if Caller == 0 or item[0] == 0:
                text += f'{i} | {item[1]}'
            elif Caller == 1:
                val = str(getattr(self.Class, *item[2]))
                text += f'{item[1]}: {val}'
            elif Caller == 2:
                _, attr = item[2]
                val = str(getattr(self.Class, attr))
                text += f'{i} | {item[1]}: {val}'
            if i+1 != len(self.Item):
                text += '\n'
        print(text)
        try:
            choice = str(input(self.inText))
            self.__Refresh()
            for item in self.Item:
                if str(item[0]) == choice:
                    func, *args = item[2]
                    if callable(func):
                        func(*args, **item[3])
                        break
                    else:
                        return
                elif '' == choice and Caller == 1:
                    return
            self.run()
        except MenuException as err:
            print(err)
            input()
            self.run()
class BasicMenu(Base):
    """Basic menu class for creating and managing menus.

    This class extends the functionality of the `Base` class by providing a way to create and manage basic menus that accept user input and call an associated function when an item is selected.

    The docstrings for this class were written by OpenAI.

    Parameters
    ----------
    Title : str
        The title of the menu.

    Attributes
    ----------
    Title : str
        The title of the menu.
    Class : object
        The class associated with the menu.
    Item : list
        A list of items in the menu, each represented as a list with the following elements:
            - The caller for the item (an integer that specifies the position of the item in the menu).
            - The text of the item.
            - The function to call when the item is selected, along with any arguments and keyword arguments.
    inText : str
        The text to display when requesting user input.

    """
    def __init__(self, Title: str):
        """
        Initialize a `BasicMenu` instance.

        Parameters
        ----------
        Title : str
            The title of the menu.

        """
        super().__init__(Title = Title)

    def add_item(self, Caller: int, Text: str, Func: object, *args, **kwargs):
        """Add an item to the menu.

        This method adds an item to the menu at the specified position. If the position is already occupied, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position at which to add the item in the menu.
        Text : str
            The text of the item.
        Func : object
            The function to call when the item is selected.
        args : tuple
            The arguments to pass to the function when the item is selected.
        kwargs : dict
            The keyword arguments to pass to the function when the item is selected.

        Raises
        ------
        CallerError
            If the specified position is already occupied.

        """
        super().add_item(Caller, Text, Func, *args, **kwargs)

    def update_item(self, Caller: int, Text: str, Func: object, *args, **kwargs):
        """Update an item in the menu.

        This method updates an item in the menu at the specified position. If the specified position does not exist, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position of the item to update in the menu.
        Text : str
            The new text of the item.
        Func : object
            The new function to call when the item is selected.
        args : tuple
            The new arguments to pass to the function when the item is selected.
        kwargs : dict
            The new keyword arguments to pass to the function when the item is selected.

        Raises
        ------
        CallerError
            If the specified position does not exist.

        """
        super().update_item(Caller, Text, Func, *args, **kwargs)
        
class InfoMenu(Base):
    """Info menu class for creating and managing menus.

    This class extends the functionality of the `Base` class by providing a way to create and manage info menus that display information without accepting user input.

    The docstrings for this class were written by OpenAI.

    Parameters
    ----------
    Title : str
        The title of the menu.
    Class : object
        The class associated with the menu.

    Attributes
    ----------
    Title : str
        The title of the menu.
    Class : object
        The class associated with the menu.
    Item : list
        A list of items in the menu, each represented as a list with the following elements:
            - The caller for the item (an integer that specifies the position of the item in the menu).
            - The text of the item.
            - The attribute of the associated class to display when the item is selected.
    inText : str
        The text to display when requesting user input.

    """
    def __init__(self, Title: str, Class: object):
        """
        Initialize a `InfoMenu` instance.

        Parameters
        ----------
        Title : str
            The title of the menu.
        Class : object
            The class associated with the menu.

        """
        super().__init__(Title = Title, Class = Class, Item = [])

    def add_item(self, Caller: int, Text: str, Attr: str):
        """Add an item to the menu.

        This method adds an item to the menu at the specified position. If the position is already occupied, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position at which to add the item in the menu.
        Text : str
            The text of the item.
        Attr : str
            The attribute of the associated class to display when the item is selected.

        Raises
        ------
        CallerError
            If the specified position is already occupied.

        """
        super().add_item(Caller, Text, Attr)

    def update_item(self, Caller: int, Text: str, Attr: str):
        """Update an item in the menu.

        This method updates an item in the menu at the specified position. If the specified position does not exist, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position of the item to update in the menu.
        Text : str
            The new text of the item.
        Attr : str
            The new attribute of the associated class to display when the item is selected.

        Raises
        ------
        CallerError
            If the specified position does not exist.

        """
        super().update_item(Caller, Text, Attr)

    def run(self):
        """Run the menu.

        This method creates the menu and displays it to the user. It handles menu exceptions and prints them to the screen.

        """
        self.inText = 'Enter to Continue'
        super().run(Caller=1)

class SettingsMenu(Base):
    """Settings menu class for creating and managing menus.

    This class extends the functionality of the `Base` class by providing a way to create and manage settings menus that accept user input and update an attribute of the associated class when an item is selected.

    The docstrings for this class were written by OpenAI.

    Parameters
    ----------
    Title : str
        The title of the menu.
    Class : object
        The class associated with the menu.

    Attributes
    ----------
    Title : str
        The title of the menu.
    Class : object
        The class associated with the menu.
    Item : list
        A list of items in the menu, each represented as a list with the following elements:
            - The caller for the item (an integer that specifies the position of the item in the menu).
            - The text of the item.
            - The function to call when the item is selected, along with the attribute of the associated class to update.
    inText : str
        The text to display when requesting user input.

    """
    def __init__(self, Title: str, Class: object):
        """
        Initialize a `SettingsMenu` instance.

        Parameters
        ----------
        Title : str
            The title of the menu.
        Class : object
            The class associated with the menu.

        """
        super().__init__(Title = Title, Class = Class)

    def add_item(self, Caller: int, Text: str, Attr: str):
        """Add an item to the menu.

        This method adds an item to the menu at the specified position. If the position is already occupied, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position at which to add the item in the menu.
        Text : str
            The text of the item.
        Attr : str
            The attribute of the associated class to update when the item is selected.

        Raises
        ------
        CallerError
            If the specified position is already occupied.

        """
        super().add_item(Caller, Text, self.__ChangeVal, Attr)

    def update_item(self, Caller: int, Text: str, Attr: str):
        """Update an item in the menu.

        This method updates an item in the menu at the specified position. If the specified position does not exist, a `CallerError` is raised.

        Parameters
        ----------
        Caller : int
            The position of the item to update in the menu.
        Text : str
            The new text of the item.
        Attr : str
            The new attribute of the associated class to update when the item is selected.

        Raises
        ------
        CallerError
            If the specified position does not exist.

        """
        super().update_item(Caller, Text, self._ChangeVal, Attr)

    def run(self):
        """Run the menu.

        This method creates the menu and displays it to the user. It handles menu exceptions and prints them to the screen.

        """
        super().run(Caller=2)

    def _ChangeVal(self, attr):
        """Update the specified attribute of the associated class.

        
        """
        new = input('New Value: ')
        setattr(self.Class, attr, new)
