# changelog

Every noteable change is logged here.

## v1.17.2

### Feature

* make abbreviation sortable (b3e7c93de81b)
* add method to sort words alphabetically (3a3164644493)
* introduce Cluster to formalize clustering (fd8cbedf6f58)
* use navigators page number to support selective processing (6b423f7f76ff)
* ensure that min elements is less one (e461df72629f)
* add minimal feature count (76ff8bb4e2b0)

### Fix

* avoid selecting empty page height (2681a016ad5c)

## v1.17.1

### Feature

* add abbreviation table parser step to groupme (335e2eb35c59)

### Fix

* skip non column layout (e640fd56470e)

## v1.17.0

### Feature

* add abbreviation step to command line interface (9042a3b522e2)
* add step to determine abbreviation likelihood (9490fd4b1e4d)
* extend blacklist for sentence parser (d535b262c9e4)
* add parser to extract lists of words and statistics from page (9da30366bfa4)
* add parser to convert texts into single words (6d65669334b7)
* add option to disable input validation (5f0a0d989e32)
* do not parse non closed sentences (1c72d9d4edfa)
* add abbreviation step to parse abbreviation out of text (6cd737dc3af3)
* add method to dump and load abbreviations (576dd45c86d1)
* extend DUDEN white list and remove duplication (1a75d2b70a0a)
* add optional position to store parse location (18d387e797ba)
* add method to split sentences into words (4ce5ef54c15d)
* add method to check for a sentence (6227b1fccbf1)
* support multiple lines (50b131af7a6c)
* add path module to access generated path (a193b8398533)
* ensure that algorithm has correct assumptions (744dd074bd13)
* use simple parser only as backup (d2bcf54d74e9)
* remove trailing white spaces of shortcut (29c7e34c3192)
* add judging strategy to abbreviation (c17202e4d26d)
* add abbreviation geometry strategy (725c3099a73b)
* add classifier to group list of number by distance (000de5d97f0d)
* sort cluster by element size descending (a3927aa65e30)
* move simple parser to first simple strategy (ba34d295add3)
* add pattern to implement abbreviation parser strategies (a61aee3a1da2)
* add simple abbreviation extractor (bbb0d56e3e25)

### Fix

* extend word splitter (b04e455cf524)
* fix cluster computation (4c84481154b4)
* increase tolerance to solve master116 example (9662a88eb4a6)
* use y1 baseline to improve grouping quality (ead0b08f8dc4)
* disable broken foot note parser test (71feecfd9221)
* change expected size to new font size rounding (5c8f7feeedd5)

### Documentation

* add introduction to introduce sections feature (9a69f4695488)

## v1.16.1

### Feature

* add distance feature to cli (1b0d5d6541f7)

## v1.16.0

### Feature

* add distance feature (18e935b39307)
* add tolerance to inside detection (05966311a689)
* extend path module (5e9a21dc0895)
* add area step to command line interface (cade977e92ad)
* save area of non textual elements (77c0d29de7df)
* add method to dump and load detected areas (ca3c67de15c0)
* add step area to judge elements on page (0141b2444a9a)
* add method to determine minimal count of required rectangles (6e063f354505)
* add bounding rectangle checker (3690735ae1ba)

### Documentation

* extend interface documentation (46bd0eaee5d6)

## v1.15.9

## v1.15.8

### Fix

* fix generated outpath names (d7e91557c390)

## v1.15.7

### Documentation

* fix title page introduction (459638064943)

## v1.15.6

### Fix

* log that textnavigator was not loaded (c00a96c1b987)

## v1.15.5

## v1.15.4

### Fix

* fix detecting page number (a75051a58bef)

## v1.15.3

### Feature

* extract raw page number and converted value (f4292cfb3e9b)
* add method to find item in navigator by BoundingBox (411607f51c0d)

## v1.15.2

## v1.15.1

### Fix

* add detector run to example data generator (3981793cb43f)

### Documentation

* add purpose of test data generator (4e5650c20864)

## v1.15.0

### Feature

* add missing resources to footer extraction step (25a4ca4b8c7e)
* use highnotes parser and modify holy notes (f521890e7cc4)
* add style to parsed footraw-note (8bd0044c32dc)
* add font information to pagetextnavigator if provided (0df71d53d10d)
* add method to parse footer with footnotes (0671139d4673)
* add method to merge highnotes in horizontal line (01808530d52b)
* add Bounding to extracted Highnote (f131c36d8c46)
* add method to split content by Highnote (0cb2d3b604b0)
* create separate package to add more detection logic (6321f606adf5)
* parse multiline footnotes (0a94785a2234)

### Fix

* fix spelling error (be363d911f4d)
* avoid determine min of empty sequence (229b43fcf9c2)
* resolve cyclic import (27f92d0fa0c7)
* do not modify parsed input data (884a683df2f5)

### Documentation

* extend interface documentation (c329e51de7ce)

## v1.14.12

## v1.14.11

## v1.14.10

### Feature

* extend pattern to parse on multiple lines. (935d092bd671)

### Fix

* extend check that lowest examiner is not detected as author (0147b9846dfc)
* extend prof-detection pattern (f9f3775111be)
* support multiline title (07045324605c)
* fix date parser (996d195216bd)
* fix accessing correct variable (271adc13f57d)

### Documentation

* extend title parser documentation (eacf2b2d71e2)

## v1.14.9

### Fix

* log page validations and do not let application fail (3914fcf2bde3)

## v1.14.8

## v1.14.7

### Feature

* add method to ensure unique pages (e4441d39b3b1)
* do not process item without and header and footer (14686d862514)
* ensure that extract gets sorted pages and produces sorted results (2c1f66572a78)
* ensure that sync gets sorted iterators (a187810d7384)
* extend person parser (f11716ac2816)

### Fix

* create correct pytest test names with forward slashs (bbdd916e41eb)
* sort results by page (79ddbffd1a9b)
* fix test after removing duplicates (b0b886828f28)
* fix pages extract to ensure sorted pages (64d12ce3c693)
* fix strategy selector (98dcf430015e)

## v1.14.6

### Documentation

* Happy New Year! (8bb16846ed5d)

## v1.14.5

## v1.14.4

## v1.14.3

### Feature

* add method to determine toc output path (16e7c42cfca4)

## v1.14.2

### Feature

* reduce example generation time due multi processing (25fb9aee9af6)

### Fix

* return None if no valid TitlePage can be selected (931d19ee3dc6)
* ignore numbered invalid dr. title (1ad4fec582c9)

## v1.14.1

### Feature

* reduce miss detection of title pages (ea5d24c098e5)

## v1.14.0

### Feature

* extend title page parser (ded7aff53250)

### Fix

* parse none existing institution as None (622f20f8113d)

## v1.13.6

### Fix

* fix problem with starting white page (2b2ab90677e6)

## v1.13.5

### Feature

* check if directory exists externally (1951cf5e46a1)

## v1.13.4

### Feature

* add `raw` and `page` to have more data for decider/validator (a7fae9bde03e)

## v1.13.3

### Fix

* report toc extraction problem instead of failing with error (05d37409fbbf)

## v1.13.2

### Fix

* enable to process all pages (e9cd3ee8c0e3)

## v1.13.1

### Feature

* add example data generator for following data unit (4ab8f384305b)

### Documentation

* add missing headline to last release page (8c217b11dd59)

## v1.13.0

### Feature

* add new table of content extraction approach (cbac8eedf3b7)
* add method to create PageTextContentNavigators (8dbd1959a88b)
* support parsing PageTextNavigator (57fba93d27e4)
* add method to split container by key function (96ed405c2a6b)
* add method to load data required by toc extractor (889ad053c49b)
* remove outdated chapter extraction approach (58652631f616)
* add geometric strategy to extract table of content (a81c1669ad04)
* add method to determine text feed of document (0ac997b3a7b4)
* add toc extraction decider strategy (03c21b5b5e8e)
* return empty list if group empty list (12e33cfc20d3)
* extend toc regex parser (fa2ac86e14c6)
* disable checking content border to parse headlines correctly (c41e741c2ad5)
* do not detect normal text as common-text-header (90918c8009a6)
* add new header extraction strategy (887046fbb784)
* use text as __repr__ for TextInfo to ease print debugging (07b02d85b48e)
* extend line parser to parse bachelor111 toc correctly (5166b213c111)
* extend toc-regex-strategy to support more pattern (afda1be76415)
* add basic toc extractor strategy (25d1c065bcf3)
* add AppendixLevel to support more toc lines (68d065abd652)
* add method to group headlines depending on chapter (eae872622d31)
* introduce regex text package to unify regex (8c4d9ba29b92)
* add toc geometry strategy (47feea746c55)
* extend regex headline parser (af0339c2f784)
* add method to parse single headline (b5e8075826fa)
* extend interface documentation (0f4052b246a9)
* add parameter to control none-ending (4d83418fa288)
* add method to create textcontentnavigator from path (ca81a8ae1fb6)
* make textnavigator creation prefix-able (0f9be2129c50)

### Fix

* parse collect content at end of loop (6c318e0092cb)
* do not shrink pages without header and footer (e106a93aa771)
* ensure that sort_byposition sorts correctly (5778c535c04c)
* fix PageTextContentNavigator to use header/footer to determine content (a3fabb733f2e)
* fix FixedFooterStrategy (0b4e6da6d654)
* do not use prefixed navigator data (69e5e57b57fc)
* fix inserting check of text bounds (96f35c24c87e)

### Documentation

* extend interface documentation (868f6746bc91)
* update doc string (36876ab907d3)
* add link to concrete class (266b481d8f21)
* add section for footer and header strategy (d7ea7a800965)
* format structure and link unit test to design decision (75bda061b073)
* improve navigation structure (8f6ec5f3c007)
* link strategy classes to documentation (75c3e778f59c)
* add basic groupme documentation structure (9ade279b8e13)

## v1.12.0

### Feature

* extend sentence parser (327ad5f068ad)
* analyse content till content ends (4a07467333da)
* add method to compare order of iamraw.Headline (361a2baeb459)
* add more complex multiline headline extractor (cadb567264c9)
* integrate multiline headline extractor (7303718265d4)
* normalize headlines to concentrate on content (7ed053708a1f)
* use font size strategy to determine headlines (c3b03e558a45)
* add first containerid to MultilineGroup (dace4b5f01e7)
* add prototype for MuliLine-Headline-Extractor (42709006dc2f)
* add method to determine sections from path (aa6873a9a04d)
* add method group multilines by line distance (ee7c899e92ef)
* add method to merge 2 groups (982901ce56a5)
* add method to group lines by gradient of line distance (ef11f9a2d144)
* add method to group text lines by font size (2e2b56a31b42)
* add method to create style without HighNotes (d6d7d88efd44)
* add method to copy TextStyle (009d0727bccc)
* extend sentence parser to parse content before loaded chapter (38b9f773b91e)
* merge sentences with headlines of to pages (7ae1190ba345)
* add methods to extract sentences and chapter content (0218406af1b5)
* reduce smallest headline size (49e32d20539a)
* add text feed to improve headline extractor strategy (3a1c0622733d)
* make sentence more robust against capitalisation (3b84685b9553)
* use new sentence splitter to split text (3ac0b96f5021)
* add method to remove high notes (82e5e8560434)
* add method to split text into sentences (b7730240651b)
* add footerlink to public interface (2f477c142aeb)
* add method to dump and load high notes (c3fa5f910bca)
* add footerlink extractor to parse text annotation from text (bdf2e38499a8)
* validate TextStyle after init to ensure correct definition (87f327b61016)
* use TextInfo information instead of FontStore definition (7f809ef33f7f)
* add method to extract HighNotes out of TextInfo (2f1469283dae)
* literature and footer reference (25ab355d8b6f)
* load required data for text processing from path (c05f2be52653)

### Fix

* fix chapter extractor (4b367d727081)
* merge sentences and headlines over pages correctly (a4c553c42599)
* fix parsing headlines before chapter starts (6480b95ad4c2)
* skip empty pages to avoid error in max calculation (26825879218c)
* correct import (3e19e804a8e7)
* fix return type of high notes extractor (9f28631fdd1c)
* extracting headlines on single page/few pages (bcc50dc497ba)
* fix unused imports (281037da4b1a)
* skip useless empty lines (1302e9cf346d)
* reduce layout offset to avoid missing last content line (3dec60786650)
* select correct page when creating PageTextNavigator selectively (8f540d6ddaf5)
* improve no-sentence message (2b37184fc62b)

### Documentation

* add design decision to introduce StrategyError (d6eb4f74d9c0)
* remove after moved to iamraw (7498c10a2cfa)
* extend interface documentation (c2b5388a31c6)
* extend interface documentation (9aea87dc9982)
* extend interface documentation (76580d18ec8c)
* use rst to document planned releases (28d1aefaa7eb)

## v1.11.0

### Feature

* support multiple sections on a single page (e18bf3a2810f)
* support multiple sections on page (12ea34e50687)
* use configo to handle holy values (97d13423bd65)
* add possible to shrink page left to right (0c8480feea82)
* add --pages information to toc feature (6028a5c05507)

### Fix

* use --all to make robust against interface changes (9bfe8f95d30d)
* correct loading order (0d30fb55a54a)
* enable undefined extraction (d8f099568691)
* fix empty style (9fcb7ed51ce3)
* activate test after improving font calculation (440efd1a43b0)
* use new font calculation (70e68c9d8d62)
* fix document with zero moving footer (811658ac1bac)

### Documentation

* fix output formatting (e6d61d9986cc)
* extend interface documentation (5be75966d391)
* extend interface documentation (9e5d466d601a)

## v1.10.0

### Feature

* skip empty pages with no ContentBorder (3fcdd09df807)
* extend headlines parser (e342d8a9c79c)
* improve footerheader judgement strategy (4a2e707cf64b)
* add title parser based on contemporary (0032c1a13991)
* limit max area of cluster to detecting equal numbers (ea18848fc4c8)
* expose max difference to improve testing/more variance (8af216486d97)
* extend footer page extraction area to match more examples (af4b3b11d00b)
* add first strategy to reduce miss extraction (d86da2a85955)
* add report to extraction strategy to determine quality of extraction (e107d6a630fc)
* refactor decider strategy (084027318c17)
* add method to create FooterHeaderDetectionStrategy from path (5894de58d20f)
* add method to create pagetextnavigator from path (946f95985ce9)
* replace with iamraw/serializeraw code (ad1bdaae212f)
* add --pages support (516c30b2b237)
* make section pages-able - move to serializeraw later (df7142749993)
* add --pages support to select pages to process (37f48c0455a9)

### Fix

* improve headline extractor (b4bddf40a0d1)
* fix docu to enable running Sphinx (f7f25cbad0a5)
* fix pagetextnavgiator creator (66de1e80fbca)

### Documentation

* fix spelling errors (812c3f4d2894)

## v1.9.0

### Feature

* extend potential footer area (3890b5ff98eb)
* extend footnotes regex to support more text data (8aa3028ae75d)
* extend footer load and dumper (fdd31976ae13)
* extend nolevel toc parser (af0180ad167f)
* support more than one header/footer area (74ad3f7b4238)
* use configo holy values and refactor FixedFooterStrategy (775a4c9ab8e5)
* use configo.holyvalue to describe holy values (725a4ebd3dc4)
* remove process-method, use result() directly (f10e4de25bd0)
* extend footer extract (c22c0bdf3ea9)
* add information of moving footer result (23e5dc746ecc)
* add footnotes extractor (09385eef21bf)
* add pagetextnavigator to Footer interface (b346a6c4998e)
* add page number strategy extractor (8457904e17ee)
* add pattern -number- as valid number pattern (151374f1fa0d)
* add options to control footer extraction (34bf991aaa44)
* enable one element cluster (10d437de9564)

### Fix

* make chapter assertion weaker, cause algorithm is really bad (61434c90fec9)
* fix fixed footer test (6498abd6c26e)
* extend possible header area to extend page number (a6a68fbac6df)
* only select result if one item matches (2232654451b8)

### Documentation

* fix spelling errors (0b49557ab28e)
* extend footer strategy documentation (e82aa0fe2b6c)
* document general and fixed footer strategy (6b4558154964)
* extend release plan (7a3ea0035f8e)
* move proposal and releases to better place (a660ad7de65e)
* reduce toc level to increase readability (3f6552dfccda)
* add first draft of release plan 1.10.0 (b454020a8b71)
* add file path of second example to moving header (631855001ba9)
* correct description of PageTextNavigator (dbff786bb629)
* add release plan for next release (b8ec820b3b94)

## v1.8.0

### Feature

* improve chapter extractor (86c175517928)
* reduce miss detection of toc lines (282ec3648d66)
* add method to count textual lines on page (33323c9a0665)
* add moving footer strategy (ed959d05aeee)
* add --test=generate to generate test resources only (ccb3d58c8638)
* add footer/header detection strategy management (b1a13e185f0c)
* add `DocumentObjectType` to determine object type on page position (dfc69228f4e7)
* expose result names of words processing to public API (b9868bd5e963)
* split strategy into 2 different approaches (10c66afa6fd5)
* extend headline parser (6e3b90c4fefa)
* add minimal required headlines to determine footer (e5688301bced)
* improve chapter detector (8993ba473018)
* improve robustness of toc regex parser (2e955765c017)

### Fix

* reduce log level of error in toc extractor (051bd9f03a50)
* handle non-level detection (da60c4367442)
* fix bounding box names (509c219cb5b2)
* ensure that text distance is positive (55506f7c9d0d)
* improve index detector (582e2d9f46c1)
* fix chapter extractor (0754c92919aa)

### Documentation

* add two proposal to describe gradient feature (92b889de0bba)
* add description to footer extraction strategies (8c85badd671c)

## v1.7.0

### Feature

* add method to parse to via regex (687eb753a78b)
* add method to create path to rawmaker-test-resources (61b727e0d554)

## v1.6.2

## v1.6.1

### Fix

* add workaround to support 'Diplomarbeit' till iamraw is patched (2c8b932fb6eb)

## v1.6.0

### Feature

* add order for more than one person without academic title (42a5a0f6dc79)
* extend person parser to support more pattern (754d21544515)
* extend person parser to support every Dipl.- title (b949859b5284)
* extend parser to parse Persons without academic title (53811cd64d93)

### Fix

* fix test resource to be in sync with pdf (3fbb4daab251)
* fix person parser without text before academic title (803ba580d840)
* ensure that order in document is preserved (6d8ace3d5e83)

### Documentation

* extend interface documentation of person parser (d898b8e59aff)

## v1.5.1

## v1.5.0

### Feature

* extend detector API with rawmaker configuration used in title extraction (f4052491791f)
* add general pattern to support Dr. med. bio. etc. (76814aee5b65)
* convert extracted TitlePage to yaml (df7fe27fd7d1)
* add work method of title parser (3446fcac1bbc)
* support date format "February 20, 2019" to use pydoc examples (d8416eae9d91)
* convert text to PageTextNavigator to use all parsing features (46da025adbc6)
* add title parser to complete parser (52684be9c585)
* activate multiprocessing and page selection (0d3ecbf59f52)
* add parser to parse title from hugest font (5af21ebf8abd)

### Fix

* handle no detected persons (38c361f9303b)
* increase the number of required digits for valid matrikel (4213b130cbba)
* add missing assertion after refactoring (5c021320f9a0)

## v1.4.0

### Feature

* add method to parse title text of title page (898365e6a8b1)
* add method to parse institute and courses of studies (248dfc715ea6)
* add method to parse the complete title page (1a5bbd2f8d4f)
* add method to split text in connected text blocks (53588f3373a9)
* add very simple parser to extract thesis type out of title page (885d6678b669)
* add method to parse matrikel number out of title page (6a3808c651c2)
* reduce required test power due reducing the count of pdfs under test (fa03e349d9de)
* add person parser to extract person with title from front-page (2f955a12f8d3)
* add parser to parse the date of title page (289ca8725aa7)
* add `detector` to analyze special features like title, toc etc. (7144438f6134)

### Fix

* fix massive interface changes after integration (e7a2917bc848)
* add missing test data generation (660377686f9d)

### Documentation

* add requirements for title parser (c4eb10ebef2a)

## v1.3.1

## v1.3.0

### Feature

* use real page size instead of constant box (981095e7e328)
* use `power` tool to generate test pdf data (cd1d689c8d14)

### Fix

* not every page contains a PageHeadlineList (b4a729861dca)
* workaround: skip broken boxed content (55d8f0939ae7)
* ignore single input file (19851678b09d)

## v1.2.10

### Feature

* extend debugging information of textprocessor (0a16551b2dde)

### Fix

* fix error in textprocessor to parse pyporting example (3eb9cc3e01db)

## v1.2.9

### Fix

* workaround: skip non content at the end (eecd435bce27)

## v1.2.8

### Fix

* add workaround to fix problem with chapter partition (7b095fdb8622)

## v1.2.7

### Feature

* extend logging to ease debugging (1276054bfae0)

### Fix

* fix headline regex to avoid enormous/infinite runtime (5d51f1c252f6)

## v1.2.6

### Feature

* add error message to assertion (177549e1a139)

## v1.2.5

## v1.2.4

## v1.2.3

## v1.2.2

### Fix

* fix output name of toc generation (a3371f9e4dae)

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
