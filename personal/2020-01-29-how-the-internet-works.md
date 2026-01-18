---
author: Alex Strick van Linschoten
categories:
  - tech
  - coding
  - technology
  - launchschool
  - internet
date: "2020-01-29"
description: "Deep dive into the layers and protocols that make the internet function, from physical infrastructure to the application level."
layout: post
title: "How the Internet Works"
toc: true
aliases:
  - "/blog/how-the-internet-works.html"
include-before-body: '<script defer data-domain="alexstrick.com" src="https://plausible.io/js/script.js"></script>'
comments:
  utterances:
    repo: strickvl/mlops-dot-systems
---

The internet. It just works. Understanding exactly *how* is a bit more complicated than many pieces of engineering. The more you examine the different aspects and parts that make it up, the more you see complexity concealed under the surface.

Visiting this website, for instance: it feels like a trivial thing to do, but there are many different parts making that happen, from the parts that actually transport the bits of data across the physical infrastructure, to the pieces that serve it all to you on a secure connection (ensuring that what I've written hasn't been altered by a third-party).

I've just finished Launch School's [LS170 module](https://launchschool.com/curriculum/courses/8cb220e7) which takes you a decent way down in the weeds to explain exactly how all of these pieces fit together to make up 'the internet'. So today I thought I'd retransmit some of that as a way of cementing it in my own mind.

At a very abstract level, the internet can be thought of as a network of networks. A network itself is a set of two or more computers which are able to communicate between each other. This could be the computers attached to a home network, or the computers that connect through a central server to a particular Internet Service Provider or ISP.

The internet makes use of a series of 'protocols', shared rules and understandings which have been developed or accreted over time. These protocols allow a computer on the other side of the planet to communicate in a mutually comprehensible manner. (If these shared sets of rules didn't exist, communicating with strangers or sending messages from one server to another would be a lot more difficult).

So once we have this top-down understanding of the internet as a bunch of networks that interact with each other, what, then, is the process by which a web browser in the United Kingdom communicates with a web server in China? Or in other words, if I want to access a website hosted on a Chinese webserver, how does that series of communication steps work to make that happen?

At this point, it's useful to make use of another abstraction: communication across the internet happens across a series of layers. There are several different models for these various layers. Two of the more common models — the OSI model and the TCP/IP model — are represented below:

![](images/2020-01-29-how-the-internet-works/927c43c6c96c_layered-system-osi-tcp-ip-comparison.avif)

At the top level — "Application" — you have your website or whatever the user comes into contact with that is being served up to your web browser, let's say. All the layers below that are progressively more and more specialised, which is another way of saying that they become progressively less comprehensible if you were to eavesdrop on the data as it were passing over the wire or through the fibre optic cable.

Let's move through the big pieces of how information is communicated, then, starting at the bottom. (I'll mostly follow the TCP/IP model since it's a bit less granular and allows me to split things up in a way that make sense). This chart will help keep all the pieces in your mind:

![](images/2020-01-29-how-the-internet-works/24852f39db7f_layersofinternet.avif)

Note that each layer has something known as a 'protocol data unit' or PDU. A PDU is usually made up of a combination of a header, payload or chunk of data and an optional footer or trailer. The header and footer contain metadata which allows for the appropriate transmission / decoding etc of the data payload.

The PDU of one layer is used by the layer below or above it to make up its own separate PDU. See the following diagram as an illustration:

![](images/2020-01-29-how-the-internet-works/30ffa3d90bfb_encapsulation.avif)

## Physical Layer

Before we get into the realm of protocols, it's worth remembering and reminding ourselves that there is a physical layer on which all the subsequent layers rely. There are *some* constraints relating to the speed or latency with which data can be transmitted over a network which relate to fixed laws of physics. The most notable of those constraints is the fact of the speed of light.

## Link Layer — Ethernet

Ethernet is the protocol that enables communication between devices on a single network. (These devices are also known as 'nodes'). The link layer is the interface between the physical network (i.e. the cables and routers) and the more logical layers above it.

The protocols for this layer are mostly concerned with identifying devices on the network, and moving the data among those devices. On this layer, devices are identified by something called a MAC (Media Access Control) address, which is a permanent address burned into every device at the time of manufacturing.

The PDU of the Ethernet layer is known as a 'frame'. Each frame contains a header (made up of a source address and a destination address), a payload of data, and a footer.

## Internet Layer — The Internet Protocol (IPv4 or IPv6)

Moving up a layer, part of the Ethernet frame is what becomes the PDU for the internet or network layer, i.e. a packet.

This internet layer uses something known as the internet protocol which facilitates communication between hosts (i.e. different computers) on *different* networks. The two main versions of this protocol are known as IPv4 and IPv6. They handle routing of data via IP addressing, and the encapsulation of data into packets.

IPv4 was the de facto standard for addresses on the internet until relatively recently. There are around 4.3 billion possible addresses using this protocol, but we are close to having used up all those addresses now. IPv6 was created for this reason and it allows (through the use of 128-bit addresses) for a massive 340 undecillion (billion billion billion billion) different addresses.

Adoption of IPv6 [is increasing](https://www.google.com/intl/en/ipv6/statistics.html), but still slow.

There is a complex system of how data makes its way from one end node on the network, through several other networks, and then on to the destination node. When the data is first transmitted, a full plan of how to reach that destination is not formulated before starting the journey. Rather, the journey is constructed ad hoc as it progresses.

## Transport Layer — TCP/UDP

There are a number of different problems that the transport layer exists to solve. Primarily, we want to make sure our data is passed reliably and speedily from one node to another through the network.

TCP and UDP are two protocols which are good at different kinds of communication. If the reliability of data transmission is important to us and we need to make sure that every piece of information is transmitted, then TCP (Transmission Control Protocol) is a good choice. If we don't care about every single piece of information — in the case of streaming a video call, perhaps, or watching a film on Netflix — but rather about the speed and the ability to continuously keep that data stream going, then UDP (User Datagram Protocol) is a better choice.

There are differences between the protocols beyond simply their functionality. We can distinguish between so-called 'connection-oriented' and 'connectionless' protocols. For connection-oriented protocols, a dedicated connection is created for each process or strand of communication. The receiving node or computer listens with its undivided attention. With a connectionless protocol, a single port listens to all incoming communication and has do disambiguate between all the incoming conversations.

TCP is a connection-oriented protocol. It first sends a three-way handshake to establish the connection, then sends the data, and sends a four-way handshake to end the connection. The overhead of having to make these handshakes at the beginning and at the end, it's a fairly costly process in terms of performance, but in many parts of internet communication we really do need all the pieces of information. Just think about an email, for example: it wouldn't be acceptable to receive only 70% of the words, would it?

UDP is a connectionless protocol. It is in some ways a simpler protocol compared to TCP, and this simplicity gives it speed and flexibility; you don't need to make a handshake to start transmitting data. On the negative side, though, it doesn't guarantee message delivery, or provide any kind of congestion avoidance or flow control to stop your receiver from being overwhelmed by the data that's being transmitted.

## Application Layer — HTTP

HTTP is the primary communication protocol used on the internet. At the application layer, HTTP provides communication of information to applications. This protocol focuses on the structure of the data rather than just how to deliver it. HTTP has its own syntax rules, where you enclose elements in tags using the `<` data-preserve-html-node="true" and `>` symbols.

Communication using HTTP takes the form of response and request pairs. A client will make a 'request' and it'll receive (barring some communication barrier) a 'response'. HTTP is known as a 'stateless' protocol in that each request and response is completely independent of the previous one. Web applications have many tricks up their sleeve to make it *seem* like the web is stateful, but actually the underlying infrastructure is stateless.

When you make an HTTP request, you must supply a path (e.g. the location of the thing or resource you want to request / access) and a request method. Two of the most common request methods are `GET` and `POST`, for requesting and amending things from/on the server respectively. You can also send optional request 'headers' which are bits of meta-data which allow for more complicated requests.

The server is obliged to send a HTTP status code in reply. This code tells you whether the request was completed as expected, or if there were any errors along the way. You'll likely have come across a so-called ['404' page](http://www.404errorpages.com/). This is referring to the `404` status code indicating that a resource or page wasn't found on the server. If the request was successful, then the response may have a payload or body of data (perhaps a chunk of HTML website text, or an image) alongside some other response headers.

Note that all this information is sent as unencrypted plain text. When you're browsing a vanilla `http://` website, all the data sent back and forth is just plain text such that anyone (or any government) can read it. This wasn't such a big issue in the early days of the internet, perhaps, but quite soon it became more of a problem, especially when it came to buying things online, or communicating securely. This is where TLS comes in.

TLS or Transport Layer Security is sometimes also known as SSL. It provides a way to exchange messages securely over an unsecured channel. We can conceptually think of it as occupying the space between the TCP and HTTP protocols (at the session layer of the OSI framework above). TLS offers:

- encryption (encoding a message so only authorised people can decode it)
- authentication (verifying the identity of a message sender)
- integrity (checking whether a message has been interfered with)

Not all three are necessarily needed or used at any one time. We're currently on [version 1.3](https://www.ietf.org/blog/tls13/) of TLS.

---

Whew! That was a lot. There are some [really good](https://www.youtube.com/watch?v=AEaKrq3SpW8) [videos](https://www.youtube.com/watch?v=x3c1ih2NJEg&t=7s) which make the topic slightly less dry. Each of these separate sections are extremely complex, but having a broad overview is useful to be able to disambiguate what's going on when you use the internet.
