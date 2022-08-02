# A. Some outline.
> Why do we need it?
> 
> What does it offer?
>
> How to extend it for extendibility?

# B. What we need.
## a. Component.
Every component must implement the serialization interface.

Every component can be extended by plugins in these areas such as appearance, feature.

We also can create our own component.

### 1. Container(custom layout).
Every component has a container to hold other components. This is designed for custom widgets of user. We can assemble our own components with exist components and reuse them with "Assembling editor" which is used to assemble components.

The layout of container can be grid layout or free layout which means we can drag other components anywhere in this container. The layout can be customized by plugin. We will offer calendar layout, timeline layout by built-in plugin.

### 2. Assembling editor.
We can custom our own component here and replace these component in the scene.

### 3. Text.
> Search and replace information.

#### 3.1. Text editor in the scene.
We need an editor to type in some rich words. The format can be rich text or markdown text.

We can copy and reference information from html and write reference address and protocol in the specific embedded widget. Or we can review html from link.

We can export text editor data to different format.

More complex features such as block text can be implemented by scene work flow. Code highlighting or hint can be extended by plugin.

#### 3.2. Cards.
Except for the editors anywhere in the scene, we also need some free cards to fix the unmanageability of excessively free coordinates.

It is the same as text editor in the scene but managed in a different way.

### 4. PDF reader.
We can open a pdf and edit it through pdf reader. Some connections can be established with components.

### 5. Resource reader.
Video, Audio.

## b. Work flow.
### 1. Knowledge.
We can create connection between any cards and component. Then the cards will show when mouse is hovering over these components.

### 2. Team.
Add someone to team and use "@someone" to remind the specific person. Collaboration between team members will be implemented with peer to peer architecture.

### 3. Git version support.
Any changes to the note will be marked.

## c. appearance.
### 1. Layout.
The window can be put anywhere.

### 2. Flying widgets.
We provide a built-in plugin to show flying custom widgets in view.

### 3. Custom appearance.
Users can change appearance of any components. Mouse click event, double click event, release event, hover event | Item movement, collision, creation, deletion.