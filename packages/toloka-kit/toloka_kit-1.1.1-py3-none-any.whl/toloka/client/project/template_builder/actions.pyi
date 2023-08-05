__all__ = [
    'BaseActionV1',
    'BulkActionV1',
    'NotifyActionV1',
    'OpenCloseActionV1',
    'OpenLinkActionV1',
    'PlayPauseActionV1',
    'RotateActionV1',
    'SetActionV1',
    'ToggleActionV1',
]
import toloka.client.project.template_builder.base
import toloka.util._extendable_enum
import typing


class BaseActionV1(toloka.client.project.template_builder.base.BaseComponent, metaclass=toloka.client.project.template_builder.base.VersionedBaseComponentMetaclass):
    """Perform various actions, such as showing notifications.
    """

    def __init__(self, *, version: typing.Optional[str] = '1.0.0') -> None:
        """Method generated by attrs for class BaseActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]


class BulkActionV1(BaseActionV1):
    """Use this component to call multiple actions at the same time, like to show more than one notification when a button is clicked.

    Actions are invoked in the order in which they are listed. This means that if two actions write a value to the same
    variable, the variable will always have the second value.
    Attributes:
        payload: An array of actions that you want to call.
    """

    def __init__(
        self,
        payload: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, typing.List[toloka.client.project.template_builder.base.BaseComponent]]] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class BulkActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    payload: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, typing.List[toloka.client.project.template_builder.base.BaseComponent]]]


class NotifyActionV1(BaseActionV1):
    """The component creates a message in the lower-left corner of the screen.

    You can set the how long the message will be active, the delay before displaying it, and the background color.
    Attributes:
        payload: Parameters for the message.
    """

    class Payload(toloka.client.project.template_builder.base.BaseTemplate):
        """Parameters for the message.

        Attributes:
            content: Message text
            theme: The background color of the message.
            delay: The duration of the delay (in milliseconds) before the message appears.
            duration: The duration of the message activity (in milliseconds), which includes the duration of the delay
                before displaying it.
                For example, if duration is 1000 and delay is 400, the message will be displayed for
                600 milliseconds.
        """

        class Theme(toloka.util._extendable_enum.ExtendableStrEnum):
            """The background color of the message.

            Attributes:
                INFO: blue
                SUCCESS: green
                WARNING: yellow
                DANGER: red
            """

            DANGER = 'danger'
            INFO = 'info'
            SUCCESS = 'success'
            WARNING = 'warning'

        def __init__(
            self,
            content: typing.Optional[typing.Any] = None,
            theme: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, Theme]] = None,
            *,
            delay: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, float]] = None,
            duration: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, float]] = None
        ) -> None:
            """Method generated by attrs for class NotifyActionV1.Payload.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        content: typing.Optional[typing.Any]
        theme: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, Theme]]
        delay: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, float]]
        duration: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, float]]

    def __init__(
        self,
        payload: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, Payload]] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class NotifyActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    payload: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, Payload]]


class OpenCloseActionV1(BaseActionV1):
    """This component changes the display mode of another component by opening or closing it.

    What happens to the component depends on the type of component:
        view.image — expands the image to full screen.
        view.collapse — expands or collapses a collapsible section of content.
    Attributes:
        view: Points to the component to perform the action with.
    """

    def __init__(
        self,
        view: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, toloka.client.project.template_builder.base.RefComponent]] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class OpenCloseActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    view: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, toloka.client.project.template_builder.base.RefComponent]]


class OpenLinkActionV1(BaseActionV1):
    """Opens a new tab in the browser with the specified web page.

    For example, you can open a link when a button is clicked.
    Attributes:
        payload: URL of the web page.
    """

    def __init__(
        self,
        payload: typing.Optional[typing.Any] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class OpenLinkActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    payload: typing.Optional[typing.Any]


class PlayPauseActionV1(BaseActionV1):
    """This component controls audio or video playback. It stops playback in progress or starts if it is stopped.

    For example, this component will allow you to play two videos simultaneously.

    You can also stop or start playback for some event (plugin. trigger) or by pressing the hotkey (plugin.hotkeys).
    Attributes:
        view: Points to the component that plays audio or video.
    """

    def __init__(
        self,
        view: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, toloka.client.project.template_builder.base.RefComponent]] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class PlayPauseActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    view: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, toloka.client.project.template_builder.base.RefComponent]]


class RotateActionV1(BaseActionV1):
    """Rotates the specified component by 90 degrees.

    By default it rotates to the right, but you can specify the direction in the payload property.
    Attributes:
        view: Points to the component to perform the action with.
        payload: Sets the direction of rotation.
    """

    class Payload(toloka.util._extendable_enum.ExtendableStrEnum):
        """An enumeration.
        """

        LEFT = 'left'
        RIGHT = 'right'

    def __init__(
        self,
        view: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, toloka.client.project.template_builder.base.RefComponent]] = None,
        payload: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, Payload]] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class RotateActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    view: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, toloka.client.project.template_builder.base.RefComponent]]
    payload: typing.Optional[typing.Union[toloka.client.project.template_builder.base.BaseComponent, Payload]]


class SetActionV1(BaseActionV1):
    """Sets the value from payload in the data in the data property.

    Attributes:
        data: Data with values that will be processed or changed.
        payload: The value to write to the data.
    """

    def __init__(
        self,
        data: typing.Optional[toloka.client.project.template_builder.base.BaseComponent] = None,
        payload: typing.Optional[typing.Any] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class SetActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    data: typing.Optional[toloka.client.project.template_builder.base.BaseComponent]
    payload: typing.Optional[typing.Any]


class ToggleActionV1(BaseActionV1):
    """The component changes the value in the data from true to false and vice versa.

    Attributes:
        data: Data in which the value will be changed. The data type must be boolean.
    """

    def __init__(
        self,
        data: typing.Optional[toloka.client.project.template_builder.base.BaseComponent] = None,
        *,
        version: typing.Optional[str] = '1.0.0'
    ) -> None:
        """Method generated by attrs for class ToggleActionV1.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    version: typing.Optional[str]
    data: typing.Optional[toloka.client.project.template_builder.base.BaseComponent]
