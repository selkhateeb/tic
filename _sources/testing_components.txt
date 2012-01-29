=========================
 Unit Testing Components
=========================


Tesing Events
-------------

DOM Level Events
================

::

  goog.events.listen(...);
  
Creating The Event Object
-------------------------

::

  Using document.createEvent(eventType)

eventType can be one of the following String values:

:"MouseEvents": Creates an instance of the MouseEvent interface.

::

  interface MouseEvent : UIEvent {
    readonly attribute long             screenX;
    readonly attribute long             screenY;
    readonly attribute long             clientX;
    readonly attribute long             clientY;
    readonly attribute boolean          ctrlKey;
    readonly attribute boolean          shiftKey;
    readonly attribute boolean          altKey;
    readonly attribute boolean          metaKey;
    readonly attribute unsigned short   button;
    readonly attribute EventTarget      relatedTarget;
    void               initMouseEvent(in DOMString typeArg, 
                                      in boolean canBubbleArg, 
                                      in boolean cancelableArg, 
                                      in views::AbstractView viewArg, 
                                      in long detailArg, 
                                      in long screenXArg, 
                                      in long screenYArg, 
                                      in long clientXArg, 
                                      in long clientYArg, 
                                      in boolean ctrlKeyArg, 
                                      in boolean altKeyArg, 
                                      in boolean shiftKeyArg, 
                                      in boolean metaKeyArg, 
                                      in unsigned short buttonArg, 
                                      in EventTarget relatedTargetArg);
  };


:"UiEvents": Creates an instance of the UiEvent interface.

::

  interface UIEvent : Event {
    readonly attribute views::AbstractView  view;
    readonly attribute long             detail;
    void               initUIEvent(in DOMString typeArg, 
                                   in boolean canBubbleArg, 
                                   in boolean cancelableArg, 
                                   in views::AbstractView viewArg, 
                                   in long detailArg);
  };


:"MutationEvents": Creates an instance of the MutationEvent interface.

::

  interface MutationEvent : Event {
  
    // attrChangeType
    const unsigned short      MODIFICATION                   = 1;
    const unsigned short      ADDITION                       = 2;
    const unsigned short      REMOVAL                        = 3;
  
    readonly attribute Node             relatedNode;
    readonly attribute DOMString        prevValue;
    readonly attribute DOMString        newValue;
    readonly attribute DOMString        attrName;
    readonly attribute unsigned short   attrChange;
    void               initMutationEvent(in DOMString typeArg, 
                                         in boolean canBubbleArg, 
                                         in boolean cancelableArg, 
                                         in Node relatedNodeArg, 
                                         in DOMString prevValueArg, 
                                         in DOMString newValueArg, 
                                         in DOMString attrNameArg, 
                                         in unsigned short attrChangeArg);
  };


:"HTMLEvents": Creates an instance of the Event interface.

::

  interface Event {
  
    // PhaseType
    const unsigned short      CAPTURING_PHASE                = 1;
    const unsigned short      AT_TARGET                      = 2;
    const unsigned short      BUBBLING_PHASE                 = 3;
  
    readonly attribute DOMString        type;
    readonly attribute EventTarget      target;
    readonly attribute EventTarget      currentTarget;
    readonly attribute unsigned short   eventPhase;
    readonly attribute boolean          bubbles;
    readonly attribute boolean          cancelable;
    readonly attribute DOMTimeStamp     timeStamp;
    void               stopPropagation();
    void               preventDefault();
    void               initEvent(in DOMString eventTypeArg, 
                                 in boolean canBubbleArg, 
                                 in boolean cancelableArg);
  };

Once we have the the event instance we need to initialze it::

  var event = document.createEvent('MouseEvents');
  event.initMouseEvent('click', //in DOMString typeArg,
                       true,    //in boolean canBubbleArg,
                       true,    //in boolean cancelableArg,
                       window,  //in views::AbstractView viewArg,
                       0,       //in long detailArg,
                       0,       //in long screenXArg,
                       0,       //in long screenYArg,
                       0,       //in long clientXArg,
                       0,       //in long clientYArg,
                       false,   //in boolean ctrlKeyArg,
                       false,   //in boolean altKeyArg,
                       false,   //in boolean shiftKeyArg,
                       false,   //in boolean metaKeyArg,
                       0,       //in unsigned short buttonArg,
                       null     //in EventTarget relatedTargetArg);
		       );
		       

Now we have the DOM event we need to dispach it.

Dispaching The Event
--------------------
Dispatching the event is the easy part. All what we need to do is find
the element that we want to dispatch the event on and call its
dispatchEvent::

  element.dispatchEvent(event);

Or if we are dispatching the event globally we can call the dispatch
function on the document object::
 
  document.dispatchEvent(event);



Component Level Events
======================

Simply using the following function::

  component.addEventListener(EventType, handler);

and fire the events using::

  component.dispatchEvent(event);

