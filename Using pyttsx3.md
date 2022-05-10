# Using pyttsx3

An application invokes the **{pyttsx3.init()}** factory function to get a reference to a **{pyttsx3.Engine}** instance. During construction, the engine initializes a **{pyttsx3.driver.DriverProxy}** object responsible for loading a speech engine driver implementation from the **{pyttsx3.drivers}** module. After construction, an application uses the engine object to register and unregister event callbacks; produce and stop speech; get and set speech engine properties; and start and stop event loops.

## The Engine factory

**{pyttsx3.init([driverName : string, debug : bool])}** → pyttsx3.Engine
Gets a reference to an engine instance that will use the given driver. If the requested driver is already in use by another engine instance, that engine is returned. Otherwise, a new engine is created.

  **Parameters: driverName** –  
    Name of the **pyttsx3.drivers** module to load and use. Defaults to the best available driver for the platform, currently:
  
- sapi5 - SAPI5 on Windows
- nsss - NSSpeechSynthesizer on Mac OS X
- espeak - eSpeak on every other platform

  **Raises:**

- debug – Enable debug output or not.
- ImportError – When the requested driver is not found
- RuntimeError – When the driver fails to initialize

## The Engine interface

**class pyttsx3.engine.Engine**  
    Provides application access to text-to-speech synthesis.

  **connect(topic : string, cb : callable)** → dict
        Registers a callback for notifications on the given topic.

    Parameters: 
       - topic – Name of the event to subscribe to.
       - cb – Function to invoke when the event fires.
    Returns: 
      A token that the caller can use to unsubscribe the callback later.

    The following are the valid topics and their callback signatures.

    started-utterance
      Fired when the engine begins speaking an utterance. The associated callback must have the folowing signature.

    onStartUtterance(name : string) → None
    Parameters: name – Name associated with the utterance.
    started-word
    Fired when the engine begins speaking a word. The associated callback must have the folowing signature.

    onStartWord(name : string, location : integer, length : integer)
    Parameters: name – Name associated with the utterance.
    finished-utterance
    Fired when the engine finishes speaking an utterance. The associated callback must have the folowing signature.

    onFinishUtterance(name : string, completed : bool) → None
    Parameters: 
    name – Name associated with the utterance.
    completed – True if the utterance was output in its entirety or not.
    error
    Fired when the engine encounters an error. The associated callback must have the folowing signature.

    onError(name : string, exception : Exception) → None
    Parameters: 
    name – Name associated with the utterance that caused the error.
    exception – Exception that was raised.
    disconnect(token : dict)
    Unregisters a notification callback.

    Parameters: token – Token returned by connect() associated with the callback to be disconnected.
    endLoop() → None
    Ends a running event loop. If startLoop() was called with useDriverLoop set to True, this method stops processing of engine commands and immediately exits the event loop. If it was called with False, this method stops processing of engine commands, but it is up to the caller to end the external event loop it started.

    Raises: RuntimeError – When the loop is not running
    getProperty(name : string) → object
    Gets the current value of an engine property.

    Parameters: name – Name of the property to query.
    Returns: Value of the property at the time of this invocation.
    The following property names are valid for all drivers.

    rate
    Integer speech rate in words per minute. Defaults to 200 word per minute.

    voice
    String identifier of the active voice.

    voices
    List of pyttsx3.voice.Voice descriptor objects.

    volume
    Floating point volume in the range of 0.0 to 1.0 inclusive. Defaults to 1.0.

    isBusy() → bool
    Gets if the engine is currently busy speaking an utterance or not.

    Returns: True if speaking, false if not.
    runAndWait() → None
    Blocks while processing all currently queued commands. Invokes callbacks for engine notifications appropriately. Returns when all commands queued before this call are emptied from the queue.

    say(text : unicode, name : string) → None
    Queues a command to speak an utterance. The speech is output according to the properties set before this command in the queue.

    Parameters: 
    text – Text to speak.
    name – Name to associate with the utterance. Included in notifications about this utterance.
    setProperty(name, value) → None
    Queues a command to set an engine property. The new property value affects all utterances queued after this command.

    Parameters: 
    name – Name of the property to change.
    value – Value to set.
    The following property names are valid for all drivers.

    rate
    Integer speech rate in words per minute.

    voice
    String identifier of the active voice.

    volume
    Floating point volume in the range of 0.0 to 1.0 inclusive.

    startLoop([useDriverLoop : bool]) → None
    Starts running an event loop during which queued commands are processed and notifications are fired.

    Parameters: useDriverLoop – True to use the loop provided by the selected driver. False to indicate the caller will enter its own loop after invoking this method. The caller’s loop must pump events for the driver in use so that pyttsx3 notifications are delivered properly (e.g., SAPI5 requires a COM message pump). Defaults to True.
    stop() → None
    Stops the current utterance and clears the command queue.

## The Voice metadata

class pyttsx3.voice.Voice
    Contains information about a speech synthesizer voice.

    age
    Integer age of the voice in years. Defaults to None if unknown.

    gender
    String gender of the voice: male, female, or neutral. Defaults to None if unknown.

    id
    String identifier of the voice. Used to set the active voice via pyttsx3.engine.Engine.setPropertyValue(). This attribute is always defined.

    languages
    List of string languages supported by this voice. Defaults to an empty list of unknown.

    name
    Human readable name of the voice. Defaults to None if unknown.

## Examples

### Speaking text

~~~python
import pyttsx3
from sympy import python
engine = pyttsx3.init()
engine.say('Sally sells seashells by the seashore.')
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
~~~

### Saving voice to a file

~~~python
import pyttsx3
engine = pyttsx3.init()
engine.save_to_file('Hello World' , 'test.mp3')
engine.runAndWait()
~~~

### Listening for events

~~~python
import pyttsx3
def onStart(name):
   print('starting', name)
def onWord(name, location, length):
   print('word', name, location, length)
def onEnd(name, completed):
   print('finishing', name, completed)
engine = pyttsx3.init()
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
~~~

### Interrupting an utterance

~~~python
import pyttsx3
def onWord(name, location, length):
   print('word', name, location, length)
   if location > 10:
      engine.stop()
engine = pyttsx3.init()
engine.connect('started-word', onWord)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
~~~

### Changing voices

~~~python
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
~~~

### Changing speech rate

~~~python
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate+50)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
~~~

### Changing volume

~~~python
engine = pyttsx3.init()
volume = engine.getProperty('volume')
engine.setProperty('volume', volume-0.25)
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
~~~

### Running a driver event loop

~~~python
engine = pyttsx3.init()
def onStart(name):
   print('starting', name)
def onWord(name, location, length):
   print('word', name, location, length)
def onEnd(name, completed):
   print('finishing', name, completed)
   if name == 'fox':
      engine.say('What a lazy dog!', 'dog')
   elif name == 'dog':
      engine.endLoop()
engine = pyttsx3.init()
engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
engine.startLoop()
~~~

### Using an external event loop

~~~python
engine = pyttsx3.init()
engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
engine.startLoop(False)
# engine.iterate() must be called inside externalLoop()
externalLoop()
engine.endLoop()
~~~

## Implementing drivers

You can implement new drivers for the pyttsx3.Engine by:

Creating a Python module with the name of your new driver.
Implementing the required driver factory function and class in your module.
Using methods on a pyttsx3.driver.DriverProxy instance provided by the pyttsx3.Engine to control the event queue and notify applications about events.

### The Driver interface

All drivers must implement the following factory function and driver interface.

pyttsx3.drivers.buildDriver(proxy : pyttsx3.driver.DriverProxy) → pyttsx3.drivers.DriverDelegate
Instantiates delegate subclass declared in this module.

Parameters: proxy – Proxy instance provided by a pyttsx3.Engine instance.
class pyttsx3.drivers.DriverDelegate
Note
The DriverDelegate class is not actually declared in pyttsx3.drivers and cannot serve as a base class. It is only here for the purpose of documenting the interface all drivers must implement.

**init**(proxy : pyttsx3.drivers.DriverProxy, *args, **kwargs) → None
Constructor. Must store the proxy reference.

Parameters: proxy – Proxy instance provided by the buildDriver() function.
destroy()
Optional. Invoked by the pyttsx3.driver.DriverProxy when it is being destroyed so this delegate can clean up any synthesizer resources. If not implemented, the proxy proceeds safely.

endLoop() → None
Immediately ends a running driver event loop.

getProperty(name : string) → object
Immediately gets the named property value. At least those properties listed in the pyttsx3.Engine.getProperty() documentation must be supported.

Parameters: name – Name of the property to query.
Returns: Value of the property at the time of this invocation.
say(text : unicode, name : string) → None
Immediately speaks an utterance. The speech must be output according to the current property values applied at the time of this invocation. Before this method returns, it must invoke pyttsx3.driver.DriverProxy.setBusy() with value True to stall further processing of the command queue until the output completes or is interrupted.

This method must trigger one and only one started-utterance notification when output begins, one started-word notification at the start of each word in the utterance, and a finished-utterance notification when output completes.

Parameters: 
text – Text to speak.
name – Name to associate with the utterance. Included in notifications about this utterance.
setProperty(name : string, value : object) → None
Immediately sets the named property value. At least those properties listed in the pyttsx3.Engine.setProperty() documentation must be supported. After setting the property, the driver must invoke pyttsx3.driver.DriverProxy.setBusy() with value False to pump the command queue.

Parameters: 
name – Name of the property to change.
value – Value to set.
startLoop()
Immediately starts an event loop. The loop is responsible for sending notifications about utterances and pumping the command queue by using methods on the pyttsx3.driver.DriverProxy object given to the factory function that created this object.

stop()
Immediately stops the current utterance output. This method must trigger a finished-utterance notification if called during on-going output. It must trigger no notification if there is no ongoing output.

After stopping the output and sending any required notification, the driver must invoke pyttsx3.driver.DriverProxy.setBusy() with value False to pump the command queue.

### The DriverProxy interface

The pyttsx3.drivers.buildDriver() factory receives an instance of a DriverProxy class and provides it to the pyttsx3.drivers.DriverDelegate it constructs. The driver delegate can invoke the following public methods on the proxy instance. All other public methods found in the code are reserved for use by an pyttsx3.Engine instance.

class pyttsx3.driver.DriverProxy
isBusy() → bool
Gets if the proxy is busy and cannot process the next command in the queue or not.

Returns: True means busy, False means idle.
notify(topic : string, **kwargs) → None
Fires a notification.

Parameters: topic – The name of the notification.
Kwargs: Name/value pairs associated with the topic.
setBusy(busy : bool) → None
Sets the proxy to busy so it cannot continue to pump the command queue or idle so it can process the next command.

Parameters: busy – True to set busy, false to set idle
