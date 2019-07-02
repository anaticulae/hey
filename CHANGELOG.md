# Changelog

Every noteable change is logged here.

## v1.0.0

### Feature

* use central constant to describe START and END of a page (e483da22dc64)

### Fix

* use new BoundingBox-API (b7030ad511c7)
* flip y-coordinate and use new BoundingBox-API (b345b3187d6d)

### Documentation

* extend interface documentation (1653b4ab9b37)

## v0.4.2

### Feature

* add method to determine font distances based on TextBounds (4f3112995622)
* determine font level based on font-size/position information (d9873544e303)
* use central roundme method to avoid code duplicates (0f7b89513623)
* ensure rawmaker version for generating test data (e193c6257036)
* add FontContentStore to analyze fonts on current content page (a36442601646)
* add method to determine fonts from text sequence (39a7ef42b7ad)
* add headline extractor - not finished yet (49be003da2aa)
* add textnavigator which ignores footer and header information (b82c5072f299)
* add method to extract footer area from page (cc6b51479033)
* add method to determine font size of normal text of document (6d822e7159cb)
* add templates for new features style, text, words (f64c5e82362d)
* add title to chapter (d16b6883c906)
* add method to extract chapter out of `Sections` (03e581891ab5)
* extend interface documentation add some assertion (d55ffbe6ca1d)
* group sections to determine document structure (b6978f174be6)
* count ". ." instead of "." (74d35becd031)
* add extraction of chapter with incomplete chapter title (12c1ed5b533e)
* add separate serializing of title and level (7bff73817054)
* add `dump_chapter` method (f692e91bd8e3)

### Fix

* fix offset index (9b89acc24639)
* fix textprocessor accessing the right token (4704f3d4ee21)
* fix font store access via fontid (9ef271d37c7b)
* fix imports to new serializeraw version (f6245ad8c480)
* fix missing refactored package (89a1cccdaa0d)
* fix __len__ method of sections (83bcd87a1db0)
* remove percentage of page number, take only full page numbers (2a8367f49fe6)
* fix to new feature interface (44ff6236456f)

### Documentation

* extend interface documentation of FontStore (1bfa5c246f53)
* extend toc interface documentation (3f13246aa9eb)
* add hint to investigate to pipeline (b2b7805b84c6)

## v0.4.1

### Feature

* extend list parser with +, -, dotted (16d29b753659)
* add feature to extract list out of documents (b491dedc4c8f)
* add method to determine font feed and font distance (6cd43c39f390)
* add text font extractor (0bb6eb60e8e1)
* extract BoundingBoxes out of PageTextNavigator (256c928b39d9)
* start new feature words as text processor (e949eff36466)

### Documentation

* add required resource in words description (d58d88ad4f24)
* add description with `words` functionality (4ec3cc3a14f6)

## v0.4.0

### Feature

* add tableofcontent and remove unused page number (c04d33eab6ec)
* extend workplan to run section feature (fe5295dc4c9b)
* add sections to combine title, index, chapter, toc (8b8a77ae320d)
* add chapter feature to determine start of chapter (7813e1acd82b)
* add recursive feature - experimental, move to utila (ce1932e9840e)
* add white page feature detector (f10d88713fcb)
* compute percent to page size and backwards (670a6053a8b9)
* add method to determine content in the middle of a page (c195c572192d)
* add footer and header extractor (99273d9bbd61)
* create work method for toc feature (bb9d5347f7f4)
* create workplan with toc, index and title (dd7424e93b78)
* add result dump to work method of title (e2a2f25f376a)
* dump result of `index` feature (53128d220e84)
* add methods to load and dump list of likelihoods (7329bf12edd3)
* add title extractor to determine the likelihood of title-page (bee7524d03c2)
* add toc extractor to compute likelihood of table of content (bc49865b3c19)
* add index locator to identify the likelihood of index-page (dc2e52950f97)
* add basic implementation of sections data structure (d1978c06e548)
* add new cmdline tool `sections` to analyse pdf structure (27302a06976c)
* remove featurepath to reduce code duplication (4e1d2fc71ce6)

### Fix

* save class name as single string (cfda1e11e54e)
* add removed chapter number again (6b1cde6b3e7f)
* add text as standard page (23b174891369)
* add missing test resources (00a5edc7a105)
* dump white page result as str (22740013416f)
* do not change the order of content (42a6aad61160)
* problems with page numbers are fixed, this is not necessary (95ed1ee33774)
* increase range of right result cause of round single entrees of list (c20c6c4dd145)
* increase malus per page, to improve title locator performance (8535305b5e73)
* fix project configuration with correct project name (88d932d6de5a)
* make groupme version equal to current hey version (94607f95bdef)

### Documentation

* update summarisation of hey (af69c36d3ca6)
* extend interface documentation (328ad364cbeb)
* extend interface document of `index` feature (acab70e7f7c9)
* extend restructured documentation (84775dbb751a)

## v0.3.0

### Feature

* extend approach to determine table of content (6e2640173603)
* sort pagenumber output by pdf-page (f2a4484e809b)
* use new feature interface for chpater, footer, toc (5446c45c74ab)
* introduce new feature pattern form utila (f3ef71e390ac)
* structure is no longer a feature, it is more supporting code (4f92c27a73a4)
* save bounding of page number (87c75e716e49)
* add method to determine page number (6a3bf2a8cc13)
* add 2 algorithms to cluster text per page and position (0bb887d31fcb)
* add method to load textpagenavigator from text/position source (c5a4b5059eee)
* add textnavigator to simple iterate depending on position (4c3d67b57077)

### Fix

* return None when no section is located on page (9d3954075479)
* allow `:` in headlines (a7225fdebdcd)
* remove final newline of textcontainer (45971fbc7c74)

### Documentation

* extend readme with basic information (b9e372cd9926)

## v0.2.6

### Fix

* use new test API (d635ea101628)

## v0.2.5

## v0.2.4

## v0.2.3

## v0.2.2

### Feature

* change command line interface to folder architecture (16bd2ac41f4b)

### Fix

* remove compression, we will use folders (627a4412b6db)

## v0.2.1

## v0.2.0

### Feature

* add chapter extractor to cmdline (a4764811ff4b)

### Fix

* remove package before test installation (97ad07d229dc)
* add missing package include (401d3d685443)

## v0.1.0

### Feature

* move groupme to hey mono repo (b643494192aa)

## v0.0.0 Initial release

