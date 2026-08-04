release-artifact:
    needs: build-matrix
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Download all workflow artifacts
        uses: actions/download-artifact@v4
        path: collected_artifacts

      - name: Create GitHub Release and Upload ISOs
        uses: softprops/action-gh-release@v2
        with:
          files: |
            collected_artifacts/**/*.iso
          generate_release_notes: true
