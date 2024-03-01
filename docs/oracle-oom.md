---
title: Out of memory
weight: 20
toc: true
draft: true
---

This is a tale of an interesting GitLab job that fails because the Linux `oom-killer` killed Maven Surefire JVM ...

<!--more-->

## Hello

code:

	@BeforeAll
	static void beforeAll() {
		printMemory();
	}

	@BeforeEach
	void beforeEach() {
		printMemory();
	}

	private static void printMemory() {
		System.out.println( "JVM Name: " + ManagementFactory.getRuntimeMBean().getName() );
		System.out.println( "Heap: " + ManagementFactory.getMemoryMXBean().getHeapMemoryUsage() );
		System.out.println( "NonHeap: " + ManagementFactory.getMemoryMXBean().getNonHeapMemoryUsage() );
	}
