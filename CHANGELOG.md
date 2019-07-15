# Changelog

Every noteable change is logged here.

## v1.2.1

## v1.2.0

### Feature

* add `words` feature to word command line tool (2b03518dbea1)
* connect text with collected lists and boxed features (ba5bfc2cd471)
* connect objects with undefined index (20d71eaa36c9)
*  extend merge_content with optional undefined index's `uindex` (a580a94a1031)
* convert lists to str (7950e900ae61)
* add ids of merged paragraphs (412af42fe44a)
* improve textnavigator (12e13d62f3a6)
* add lru cache to improve speed (1357cf7cf7f8)
* use @checkdatatype feature to ensure data input (d883d9bf2f8b)
* add boxed-feature to `words` executable (7405a621ef91)
* add method to lookup boxid to `BoundingBox` (a695103afd98)
* add feature to extract boxes from document (3535f1d95201)
* add hint of page for skipped item (eaf2944fcbcf)
* add list to workplan/command line interface (1b09ddeb8a7f)

### Fix

* print skipped content on info level only (6031f5cd9c5e)
* decrease level of logging to reduce verbosity of logging (87aeeecc4909)
* skip non parsed area (7cc2933163f0)
* set default value for non existing header or footer (9c56180f983d)
* remove index output check - not every document contains a document (4f23ceac766b)
* enable using raw inputs instead of objects (36c562dda2a5)

### Documentation

* extend interface documentation (5d59f5983ec5)
* replace print with p to avoid collecting when searching `print` (1f375b2641b1)

## v1.1.0

### Feature

* ensure that passed border and horizontals are resources (8175a0eebf26)
* use contentborder to determine the correct undefined index (2dd24d487f0e)
* add method to dump and load extract list result (93801ffa7e1c)
* add method to extract lists (f2f43071df14)
* add text feed text detection `merge_content` (9d59df827a83)
* extend list extractor (95c597269675)
* add possible space to detection pattern (cef71ddda0a6)
* extend parser with plus, minus and dotted parser (1e52bea95218)
* add undefined to content converter (52f210c3de38)
* reduce confusion when initializing PageTextContentNavigator (af2c2a27d877)
* add ? to mark that result is not clear (84136bc7d83d)
* add parsing non headline page and reorder class (b73741344e65)
* set default container to None to fail faster (2a8efa8763d8)
* add collect on pages without any headline but text content (21b985d7e514)
* add text and text- and headlines-extractor to working plan (aa8dbcd5528d)
* add method to extract text and detect non text areas (76fdf318d7f1)
* fontstore - provide offset as class property (b3da3cabf3d3)
* add method to join multiple list to one list (b07ebfee36e2)
* add method to determine fontid of Font (ea478b459b27)
* add field page to headline (85ac9a39ce1c)
* remove None elements from white pages output (5ef13af1d62c)
* add work method to use headlines in command line tool (4855c5516818)
* don't write entree for empty page/input (b662c4871a0b)
* expand method to dump and load sections (55378678e006)
* add method to dump and load headlines (dd14a30dc538)
* save containerid for grouping text areas (d649ce931448)

### Fix

* fix list pattern detector (03944c60798f)
* fix offset bug (35b70d7f4fd3)
* fix multiple parser (80408b299fe9)
* rename field to chapter (af49c6abdc63)
* fix passing empty elements to max size detection (211c75f7fbcb)
* fix chapter index offset (e50b5f842ba0)
* fix extracting all chapter (e3dfd023299a)

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

